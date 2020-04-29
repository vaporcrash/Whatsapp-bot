from pymongo.errors import DuplicateKeyError
import logging

logger = logging.getLogger(__name__)

class QuizMongoClient:

    def __init__(self,mgdb_client,db_name):
        self.client = mgdb_client
        self.db = self.client[db_name]

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

    def retrieve_question(self,question_id):
        print(question_id)
        success = self.db["questions"].find_one(question_id)
        print(success)
        return question_id

    def update_question(self,question_id,update_doc):
        print(question_id)
        success = self.db["questions"].update_one(filter=question_id,update={'$set':update_doc})
        print(success)
        return question_id




