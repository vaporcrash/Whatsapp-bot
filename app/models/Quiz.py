

class Quiz:

    def __init__(self,db_client):
        self.db = db_client






    def load_from_cmd_line(self,**kwargs):
        """
        create quiz document.
        for each question/answer pair in list, insert entry into questions collection.
        Store all question_ids in the quiz document
        :param kwargs:
        :return:
        """
        return