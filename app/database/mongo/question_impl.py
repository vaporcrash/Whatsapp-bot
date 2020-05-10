from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import logging,time
from functools import lru_cache
import random
logger = logging.getLogger(__name__)

class QuizMongoClient:

    def __init__(self,mgdb_client:MongoClient,db_name):
        self.client = mgdb_client
        self.db = self.client[db_name]
        self.groups = self.db["groups"]

    def insert_question(self,question_doc):
        try:
            success = self.db["questions"].insert_one(question_doc)
            return success
        except DuplicateKeyError:
            logger.error("This question already exists!!")
            raise

    def delete_question(self,question_id):
        print(question_id)
        success = self.db["questions"].delete_one(question_id)
        print(success)
        return question_id

    def retrieve_question_by_id(self, question_id):
        q = {"question_id" : question_id}
        success = self.db["questions"].find_one(q)
        print(success["question_id"])
        return success if success else None

    def retrieve_question(self,question_doc):
        success = self.db["questions"].find_one(question_doc)
        print(success["question_id"])
        return success if success else None

    def update_question(self,question_id,update_doc):
        print(question_id)
        success = self.db["questions"].update_one(filter=question_id,update={'$set':update_doc})
        print(success)
        return question_id


    def get_all_group_ids(self):
        project = {
            "group_chat_id" : 1,
            "_id" : 0
        }
        result = self.groups.find(projection=project)
        return list(result)


    def get_quiz_by_name(self,name):
        find = {"quiz_name":name}
        result = self.db["quiz"].find_one(find)
        return result if result else None

    def create_new_session(self,session_doc,result_doc):
        try:
            success = self.db["sessions"].insert_one(session_doc)
            if success:
                success = self.db["results"].insert_one(result_doc)

            return success
        except DuplicateKeyError:
            logger.error("Another quiz is active!!")
            raise

    # @lru_cache(maxsize=10)
    def get_active_session(self):
        logger.debug("got_called for no reason")
        find = {"is_active" : 1}
        session = self.db["sessions"].find_one(find)
        return session or None

    def stop_active_session(self):

        filter_doc = {"is_active":1}
        update_doc = {"is_active": -1 * random.randint(1,5000)}
        self.db["sessions"].find_and_modify(filter_doc,update_doc)
        logger.debug("Updated active session and active results to random number")
        return


    def get_participants(self):
        find = {"is_active": 1}
        session = self.db["sessions"].find_one(find)
        if session:
            return session["participants"]
        return []

    def update_active_groups(self,group_id,group_name,session_id):
        filter_doc = {"_id" : session_id}
        update = {'$addToSet': {'participants': group_id},
                  "$set" : {"group_name.{}".format(str(group_id)):group_name}
                  }
        self.db["sessions"].find_one_and_update(filter_doc,update)
        return


    def update_evaluation_map(self,routing_map):
        filter_doc = {"is_active":1}
        update = {"$set" : {"routing" : routing_map }}
        self.db["sessions"].update_one(filter_doc,update)
        return

    def get_routing_map(self):
        filter_doc = {"is_active": 1}
        session_doc = self.db["sessions"].find_one(filter_doc)
        return session_doc["routing"] if session_doc else {}

    def initialize_score(self,group_id,score):
        filter_doc ={"is_active" :1}
        path = "scores.{}".format(group_id)
        update_doc = {"$set" : {path:0}}
        self.db['results'].update_one(filter_doc,update_doc)

    def get_scores(self):
        filter_doc = {"is_active": 1}
        results_doc = self.db["results"].find_one(filter_doc)
        return results_doc if results_doc else None

    def atomic_score_inc(self,group_id,increment):
        path = "scores.{}".format(group_id)
        while True:
            scores = self.get_scores()
            prev_score = scores["scores"][group_id]
            last_updated = scores["updated_at"]

            filter_doc = {"is_active": 1,path:prev_score,"updated_at":last_updated}
            update_doc = {"$set": {path: int(prev_score)+int(increment)}}
            success = self.db["results"].find_and_modify(filter_doc,update_doc)
            if success:
                break

        return

    def update_last_question_flags(self):
        timestamp = time.time()
        filter_doc = {"is_active": 1}
        update_doc = {"$set" :{"last_question_sent":timestamp}}
        self.db["sessions"].find_and_modify(filter_doc,update_doc)
        return

    def last_question_timestamp(self):

        filter_doc = {"is_active": 1}
        result = self.db["sessions"].find_one(filter_doc)
        return result["last_question_sent"] if result else None

    def atomic_score_dec(self, group_id, decrement):
        path = "scores.{}".format(group_id)
        while True:
            scores = self.get_scores()
            prev_score = scores["scores"][group_id]
            last_updated = scores["updated_at"]

            filter_doc = {"is_active": 1, path: prev_score, "updated_at": last_updated}
            update_doc = {"$set": {path: prev_score - decrement}}
            success = self.db["results"].find_and_modify(filter_doc, update_doc)
            if success:
                break

        return




if __name__ == '__main__':
    from pymongo import MongoClient
    from app.config import configurations
    db = QuizMongoClient(MongoClient(configurations.mongo_uri),configurations.mongo_db_name)
    print(db.get_all_group_ids())