import os
from app.database.mongo.constants import MONGODB,DB_CHOICE
from app.database.mongo.question_impl import QuizMongoClient
from app.config import configurations
from pymongo import MongoClient


def get_db_client():
    db_choice = os.environ[DB_CHOICE] if DB_CHOICE in os.environ else MONGODB
    if db_choice == MONGODB:
        return QuizMongoClient(MongoClient(configurations.mongo_uri),configurations.mongo_db_name)


print("initializing {}".format(__name__))
