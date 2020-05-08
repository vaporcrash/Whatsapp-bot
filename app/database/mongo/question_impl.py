from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import logging

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

    def insert_new_session(self,session_doc):
        try:
            success = self.db["sessions"].insert_one(session_doc)
            return success
        except DuplicateKeyError:
            logger.error("Another quiz is active!!")
            raise

    def get_active_session(self):
        find = {"is_active" : 1}
        session = self.db["sessions"].find_one(find)
        return session or None

    def update_active_groups(self,group_id,session_id):
        filter = {"_id" : session_id}
        update = {'addToSet': {'participants': group_id}}
        self.db["sessions"].find_one_and_update(filter,update)
        return

if __name__ == '__main__':
    from pymongo import MongoClient
    from app.config import configurations
    db = QuizMongoClient(MongoClient(configurations.mongo_uri),configurations.mongo_db_name)
    print(db.get_all_group_ids())