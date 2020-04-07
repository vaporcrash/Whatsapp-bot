import time

class Question:

    expected_attributes = ["question","answers","question_type","difficulty","category","created_by"]

    def __init__(self,*args,**kwargs):
        self.db = None

    def validate(self,data):
        if all([attr in data for attr in self.expected_attributes]):
            return True
        raise Exception

    def create_question(self,**kwargs):
        self.validate(kwargs)
        self.question = kwargs["question"].lower()
        self.answers = kwargs["answers"].lower()
        self.question_type = kwargs["question_type"].lower()
        self.difficulty = kwargs["difficulty"]
        self.category = kwargs["category"].lower()
        # TODO : created_by field will be a phone number. we can lookup admin name using this.
        self.created_by = kwargs["created_by"]
        self.timestamp = time.time()
        return
