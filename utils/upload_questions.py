"""
Script expects folder with following structure :
questions/1.jpeg
questions/2.jpeg

answers/1.jpeg
answers/2.jpeg

Will load pairs into MongoDB in Binary Format

To run :

 python -m utils.upload_questions -n test_quiz -i data -c askproxy

"""

import os
import argparse
from app.models import Quiz
from app.database import get_db_client


def read_image_dir(img_dir_path):

    num_questions = len(os.listdir(img_dir_path))
    questions = []
    for i in range(num_questions):
        q_path = "{}/questions/{}.jpeg".format(img_dir_path,(i+1))
        a_path = "{}/answers/{}.jpeg".format(img_dir_path,(i+1))
        if not os.path.exists(q_path) or not os.path.exists(a_path):
            raise Exception("Either question or answer missing for {} ".format((i+1)))
        questions.append((q_path,a_path))

    return questions


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', action='store', dest='quiz_name',
                        help='name of quiz to create',required=True)
    parser.add_argument('-i', action='store', dest='image_dir',
                        help='directory in which images for Q&A are stored',required=True)
    parser.add_argument('-c', action='store', dest='quiz_creator',
                        help='name of quiz creator',required=True)

    args = parser.parse_args()

    quiz = Quiz(db_client=get_db_client())

    quiz.load_from_cmd_line(name=args.quiz_name, questions=read_image_dir(args.image_dir)
                            , creator=args.quiz_creator)


if __name__ == '__main__':
    main()

