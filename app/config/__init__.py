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

        self.quiz_masters_by_name = config_json["masters"].keys()
        self.quiz_masters_by_id = [config_json["masters"][x]["id"] for x in config_json["masters"].keys()]
        self.group_to_master ={}
        for master in config_json["masters"]:
            for group in config_json["masters"][master]["groups_assigned"]:
                self.group_to_master[group] = config_json["masters"][master]

        self.master_groups = set(config_json["master_groups"])

configurations = Config()

if __name__ == '__main__':
    """
    if you want to test just this file, you can run the file directly
    """


