import os
import json

environment = os.environ.get("ENV") if "ENV" in os.environ else "dev"

class Config:
    def __init__(self):
        path  = "{}/{}.json".format(os.path.dirname(__file__),environment)

        config_json = json.load(open(path))
        self.mongo_uri = config_json["mongo"]["url"]
        self.mongo_db_name = config_json["mongo"]["database"]

        self.telegram_url = "{}{}".format(config_json["telegram"]["url"],config_json["telegram"]["token"])


configurations = Config()

if __name__ == '__main__':
    """
    if you want to test just this file, you can run the file directly
    """


