import logging,time
from abc import ABC,abstractmethod
from requests import Session
from functools import partial
from app.exceptions import TelegramSendError,QuizErrors
from app.config import configurations

from app.database.mongo.question_impl import QuizMongoClient
from app.database import get_db_client

logger = logging.getLogger(__name__)


class SuperBot(ABC):

    def __init__(self):
        self._url = configurations.telegram_url
        self._photo_url = "{}/sendPhoto".format(configurations.telegram_url)
        self._text_url = "{}/sendMessage".format(configurations.telegram_url)
        self.max_retries = 3
        self.session = Session()


    def send_photo_id(self,destination,photo_id):

        params = {
            "chat_id" : destination,
            "photo_id" : photo_id
        }
        self.send(destination,self._photo_url,params,{})

    def send_text(self,destination,body):
        message = {
            "chat_id" : destination,
            "text" : body
        }
        self.send(destination,self._text_url,{},message)

    def send(self,destination,url,params,message):
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

    # @abstractmethod
    # def handle_message(self,*args,**kwargs):
    #     ...

class PlayerBot(SuperBot):
    def __init__(self,db_client:QuizMongoClient):
        super().__init__()
        self.db_client = db_client

    def handle_ready_message(self,group_id):
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
        self.db_client.update_active_groups(group_id,session["_id"])
        return

    def handle_score_request(self,*args,**kwargs):
        return

    def handle_answer_message(self,*args,**kwargs):
        return


class QuizMasterBot(SuperBot):

    def __init__(self, db_client: QuizMongoClient):
        super().__init__()
        self.db_client = db_client

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

        self.db_client.insert_new_session(session_doc)
        logger.info("Sucessfully inserted new session")
        return








class MaestroBot(SuperBot):

    def __init__(self,quiz_name):
        self.db_client = get_db_client()
        self._quiz_name = quiz_name


    def run(self):
        session_doc = self.db_client.get_active_session()
        # for question in session_doc[""]



