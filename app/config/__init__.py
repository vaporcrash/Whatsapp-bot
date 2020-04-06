import os
import json


environment = os.environ.get("ENV") if "ENV" in os.environ else "dev"


class Config():

    def __init__(self):
        mongo_config_json = json.loads("{}/{}.json".format(os.path.curdir,environment))

        self.mongo_uri = "mongodb://{}:{}/{}"






