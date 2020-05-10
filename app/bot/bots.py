import time
from io import BytesIO
import logging,time,base64
from PIL import Image
from abc import ABC,abstractmethod
from requests import Session
from functools import partial,lru_cache
from app.exceptions import TelegramSendError,QuizErrors
from app.config import configurations
from matplotlib.figure import Figure



from app.database.mongo.question_impl import QuizMongoClient
from app.database import get_db_client

logger = logging.getLogger(__name__)


class SuperBot(ABC):

    QUESTION_TIMEOUT = 90
    def __init__(self):
        self._url = configurations.telegram_url
        self._photo_url = "{}/sendPhoto".format(configurations.telegram_url)
        self._text_url = "{}/sendMessage".format(configurations.telegram_url)
        self.max_retries = 3
        self.session = Session()


    def send_photo_blob(self,destination,photo_blob):

        params = {
            "chat_id" : destination
        }
        files ={
            "photo" : base64.b64decode(photo_blob)
        }
        self.send_multipart(destination,self._photo_url,params,files)


    def send_multipart(self,destination,url,params,files):
        for i in range(self.max_retries):
            try:
                response = self.session.post(url, params=params, files=files, timeout=30)
                if response.status_code == 200:
                    return response.json()
                else:
                    raise TelegramSendError(
                        "Dest : {} , Status : {} , Body : {}".format(destination, response.status_code,
                                                                     response.content))
            except TimeoutError:
                logging.error("Message to {} failed. retry {}".format(destination, (i + 1)))
                i += 1

        raise TelegramSendError("Dest : {}  Timeout after {} tries!!! ".format(destination, self.max_retries))


    def send_photo_id(self,destination,photo_id):

        params = {
            "chat_id" : destination,
            "photo_id" : photo_id
        }
        self.send_json(destination,self._photo_url,params,{})

    def send_text(self,destination,body):
        message = {
            "chat_id" : destination,
            "text" : body
        }
        self.send_json(destination,self._text_url,{},message)

    def send_json(self,destination,url,params,message):
        for i in range(self.max_retries):
            try:
                response = self.session.post(url,params=params,json=message,timeout=30)
                if response.status_code == 200:
                    return response.json()
                else:
                    raise TelegramSendError("Dest : {} , Status : {} , Body : {}".format(destination,response.status_code,response.content))
            except TimeoutError:
                logging.error("Message to {} failed. retry {}".format(destination,(i+1)))
                i+=1

        raise TelegramSendError("Dest : {}  Timeout after {} tries!!! ".format(destination,self.max_retries))

    def broadcast_message(self,url:str,destinations:list,params:dict,body:dict):
        f = partial(self.send,url=url,params=params,body=body)
        map(f,destinations)

    def broadcast_photos(self,destinations,photo):
        f = partial(self.send_photo_blob,photo_blob=photo)
        map(f,destinations)
        return

    # @abstractmethod
    # def handle_message(self,*args,**kwargs):
    #     ...

class PlayerBot(SuperBot):
    def __init__(self,db_client:QuizMongoClient):
        super().__init__()

        self.db_client = db_client
        self._masters = configurations.quiz_masters_by_id

    @lru_cache(maxsize=10)
    def get_routing_details(self):
        logger.info("Calling this method again!!")
        return self.db_client.get_routing_map()


    def find_master_for_eval(self,participant):
        return self.get_routing_details()[str(participant)]


    def handle_ready_message(self,group_id,group_name):
        """
        update the current session object in mongo with this group id
        :param group_id:
        :return:
        """

        # get current session
        session = self.db_client.get_active_session()
        if not session:
            raise QuizErrors.NoActiveSessions()

        #update session with group id
        self.db_client.update_active_groups(group_id,group_name,session["_id"])
        self.db_client.initialize_score(group_id,0)
        return

    def handle_score_request(self,group_id):
        scores_doc = self.db_client.get_scores()
        session_doc = self.db_client.get_active_session()
        logger.debug("Got the score!")
        fig = Figure()
        ax = fig.subplots()
        scores = scores_doc["scores"]
        ax.barh(list(scores.keys()), list(scores.values()), color='g')
        print(session_doc)
        team_names = [session_doc["group_name"][x] for x in scores.keys()]
        ax.set_yticklabels(team_names)
        ax.set_xlabel('Scores')
        ax.set_title('Current Score')
        figfile = BytesIO()
        fig.savefig(figfile, format='png')
        logger.debug("Created the plot!")
        figfile.seek(0)  # rewind to beginning of file
        files = {"photo" : figfile.getvalue() }
        self.send_multipart(group_id, self._photo_url, {"chat_id":group_id}, files)
        logger.debug("Sent back the score!")
        return

    def time_since_question(self):
        last_question = self.db_client.last_question_timestamp()
        if time.time() - last_question > self.QUESTION_TIMEOUT:
            return "TIMEDOUT !! "
        return ""

    def handle_answer_message(self,group_id,group_name,text):
        dest = self.find_master_for_eval(group_id)
        its_too_late = self.time_since_question()
        updated_text = "{}| {}\t#{}: \n{}".format(its_too_late,group_name,group_id,text)
        self.send_text(dest,updated_text)
        return


class QuizMasterBot(SuperBot):

    def __init__(self, db_client: QuizMongoClient):
        super().__init__()
        self.db_client = db_client

    #
    # def generate_file_id(self,questions):
    #     """
    #     uploads each question to Telegram and recieves file id.
    #     stores filed id instead of question blob
    #     :param questions:
    #     :return:
    #     """
    #     updated_questions = []
    #     for questions in questions:
    #         self.uplo


    def assign_players_to_master(self):
        """
        go through list of pariticipating groups and divide them equally to players
        :return:
        """
        masters = configurations.quiz_masters_by_id
        participants = self.db_client.get_participants()
        routing = {}

        for i,group in enumerate(participants):
            routing[str(group)] = masters[i % len(masters)]

        logger.debug("Evaluation map : {}".format(routing))
        self.db_client.update_evaluation_map(routing)


    def time_to_prepare(self,quiz_name):
        """
        Create a new session object and mark active to True
        :param msg:
        :return:
        """
        #read quiz from db
        quiz_doc = self.db_client.get_quiz_by_name(quiz_name)
        logger.debug("Found {} in backend!".format(quiz_name))
        if not quiz_doc:
            raise QuizErrors.QuizNotFound("{} not found".format(quiz_name))

        def strip_question_doc(q_doc):
            return {
                "question" : q_doc["question"],
                "answer" : q_doc["answer"]
            }

        #get questions and copy them to session
        questions = [strip_question_doc(self.db_client.retrieve_question_by_id(q_id)) for q_id in quiz_doc["questions"]]
        logger.info("Found {} questions!".format(len(questions)))

        session_doc = {
            "quiz_name" : quiz_name,
            "quiz_id" : quiz_doc["_id"],
            "is_active" : 1,
            "current_question" : 0,
            "questions" : questions,
            "participants" : [],
            "scores" : [],
            "started_at" : time.time()
        }

        result_doc = {
            "is_active" : 1,
            "scores" : {},
            "question_history" : {},
            "updated_at" : str(time.time())
        }
        self.db_client.create_new_session(session_doc,result_doc)

        logger.info("Sucessfully inserted new session")
        return


    def update_score(self,group_id,score,question_num,operation="add"):
        self.db_client.atomic_score_inc(group_id,score)
        return

    def stop_quiz(self):
        self.db_client.stop_active_session()


class MaestroBot(SuperBot):

    def __init__(self):
        super().__init__()
        self.db_client = get_db_client()
        self._players = []
        logger.debug("Started Maestro!")

    def send_image_to_all(self,image):
        for player in self._players:
            self.send_photo_blob(player,image)
            logger.debug("Successfully sent photo to {}".format(player))

    def send_text_to_all(self,text):
        for player in self._players:
            self.send_text(player,text)
            logger.debug("Successfully sent closed to {}".format(player))

    def run(self):
        session_doc = self.db_client.get_active_session()
        self._players = session_doc["participants"]
        logger.debug("Got players : {}".format(self._players))
        for i,question_doc in enumerate(session_doc["questions"]):
            # update timestamp of last question. will be used to disqualify late answes
            self.db_client.update_last_question_flags()
            logger.debug("Updated last question flag ")
            # check input queue if pause or quit flag is set
            self.send_image_to_all(question_doc["question"])
            # self.broadcast_photos(self._players,question_doc["question"])
            self.send_text_to_all("10 seconds")
            time.sleep(self.QUESTION_TIMEOUT)
            self.send_text_to_all("Time up! Question closed!")
            time.sleep(30)
            self.send_image_to_all(question_doc["answer"])
            time.sleep(30)

        self.send_text_to_all("That's a wrap folks!")
        logger.debug("Completed Asking all questions!!")
