from flask import Flask
from json import JSONEncoder
from bson  import json_util
import logging
# define a custom encoder point to the json_util provided by pymongo (or its dependency bson)

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj): return json_util.default(obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

from app.database import get_db_client
db = get_db_client()

app.logger.setLevel(logging.DEBUG)
