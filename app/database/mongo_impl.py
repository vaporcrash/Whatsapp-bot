from pymongo import MongoClient
from app.config import Config

class QuizMongoClient:

    def __init__(self,uri,db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_question(self,question_doc):
        success = self.db["questions"].insert_one(question_doc)
        print(success)
        return question_doc







