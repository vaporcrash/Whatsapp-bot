import os
from .constants import MONGODB,DB_CHOICE
from .mongo_impl import MongoClient
from app.config import configurations


def get_db_client():
    db_choice = os.environ[DB_CHOICE] if DB_CHOICE in os.environ else MONGODB
    if db_choice == MONGODB:
        return MongoClient(configurations.mongo_uri,configurations.mongo_db_name)


db_client = get_db_client()
