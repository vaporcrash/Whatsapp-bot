import time
import hashlib
from bson.objectid import ObjectId

class Question:

    expected_attributes = ["question","answers","question_type","points","category","created_by"]

    def __init__(self,db_client):
        self.db = db_client

    def validate(self,data):
        if all([attr in data for attr in self.expected_attributes]):
            return True
        print(data.keys())
        raise Exception

    def transform_request(self,question_body):
        return {
            "question" : question_body["question"].lower(),
            "question_hash" : str(hashlib.md5(question_body["question"].encode()).hexdigest()),
            "answers" : [[a.lower() for a in answer] for answer in question_body["answers"]],
            "points" : question_body["points"],
            "question_type" : question_body["question_type"].lower(),
            "category" : question_body["category"].lower(),
            # TODO(ROKI) : created_by field will be a phone number. we can lookup admin name using this.
            "created_by" : question_body["created_by"],
            "timestamp" : time.time()
        }


    def create_question(self,question_body):
        self.validate(question_body)
        question_doc = self.transform_request(question_body)
        result = self.db.insert_question(question_doc)
        return result

    def delete_question(self,question_body):
        qid={"_id":ObjectId(question_body["question_id"])}
        result = self.db.delete_question(qid)
        return result

    def retrieve_question(self,question_body):
        qid={"_id":ObjectId(question_body["question_id"])}
        result = self.db.retrieve_question(qid)
        return result

    def update_question(self,question_body):
        qid={"_id":ObjectId(question_body["question_id"])}
        update_doc = question_body.pop("question_id")
        result = self.db.update_question(qid,update_doc)
        return result


if __name__ == '__main__':
    q = Question(None)

