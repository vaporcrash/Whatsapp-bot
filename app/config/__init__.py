import os
import json


environment = os.environ.get("ENV") if "ENV" in os.environ else "dev"


class Config:
    def __init__(self):
        config_json = json.loads("{}/{}.json".format(os.path.curdir,environment))
        self.mongo_uri = "mongodb://{}:{}".format(config_json["mongo"]["url"],
                                                  config_json["mongo"]["port"])
        self.mongo_db_name = config_json["mongo"]["database"]



configurations = Config()








