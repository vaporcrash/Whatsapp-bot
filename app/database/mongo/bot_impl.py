from pymongo.errors import DuplicateKeyError
import logging

logger = logging.getLogger(__name__)

class QuizMongoClient:

    def __init__(self,mgdb_client,db_name):
        self.client = mgdb_client
        self.db = self.client[db_name]
