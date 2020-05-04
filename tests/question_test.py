import json
import unittest
import mongomock
from app.models import Question
from app.database.mongo.question_impl import QuizMongoClient
from pymongo import ASCENDING
from bson import ObjectId

class QuestionsCrudTest(unittest.TestCase):

    def setUp(self):
        super(QuestionsCrudTest, self).setUp()
        self.client = mongomock.MongoClient()
        self.client["quiz_db"]["questions"].create_index([('question_hash', ASCENDING)], unique=True)
        self.qdb = QuizMongoClient(self.client,"quiz_db")


    def test_create(self):
        with open("resources/create_question.json") as fp:
            test_input = json.load(fp)
        ques = Question(self.qdb)

        # insert a question into mock mongo
        result = ques.create_question(test_input)

        # query mock mongo to see if question exists
        ins = self.client["quiz_db"]["questions"].find_one({"_id":ObjectId(result.inserted_id)})
        self.assertEqual(ins["question_hash"], "17f7b9742d27830356fc49436dd04063")

    def test_duplicate(self):
        with open("resources/create_question.json") as fp:
            test_input = json.load(fp)
        ques = Question(self.qdb)
        ques.create_question(test_input)
        with self.assertRaises(mongomock.DuplicateKeyError):
            ques.create_question(test_input)


    def tearDown(self) -> None:
        super().tearDown()
        self.client.close()


if __name__ == '__main__':
    unittest.main()
