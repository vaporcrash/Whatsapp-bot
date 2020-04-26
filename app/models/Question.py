import time
import hashlib

class Question:

    expected_attributes = ["question","answers","question_type","difficulty","category","created_by"]

    def __init__(self,db_client):
        self.db = db_client

    def validate(self,data):
        if all([attr in data for attr in self.expected_attributes]):
            return True
        print(data.keys())
        raise Exception

    def create_question(self,question_body):
        self.validate(question_body)


        question_doc = {
            "question" : question_body["question"].lower(),
            "question_hash" : str(hashlib.md5(question_body["question"].encode()).hexdigest()),
            "answers" : list(map(lambda x:x.lower(),question_body["answers"])),
            "question_type" : question_body["question_type"].lower(),
            "difficulty" : question_body["difficulty"],
            "category" : question_body["category"].lower(),
            # TODO : created_by field will be a phone number. we can lookup admin name using this.
            "created_by" : question_body["created_by"],
            "timestamp" : time.time()
        }

        result = self.db.insert_question(question_doc)
        return result


if __name__ == '__main__':
    q = Question(None)
