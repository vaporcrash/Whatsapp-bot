import os
from app.database.mongo.constants import MONGODB,DB_CHOICE
from app.database.mongo.question_impl import QuizMongoClient
from app.config import configurations
from pymongo import MongoClient

def get_db_client():
    db_choice = os.environ[DB_CHOICE] if DB_CHOICE in os.environ else MONGODB
    if db_choice == MONGODB:
        mclient = QuizMongoClient(MongoClient(configurations.mongo_uri),configurations.mongo_db_name)
        return mclient

print("running {}".format(__name__))
db_client = get_db_client()
