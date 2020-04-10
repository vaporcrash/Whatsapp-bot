from app import app,db
import json
from flask import request,jsonify,make_response
from app.models import Question


questions = Question(db)


@app.route("/")
def health():
    return "Alive and kicking!"

@app.route("/question",methods=["POST"])
def question_opertaions():

    # if request.method == "POST":
    body = request.json
    response = questions.create_question(body)
    print(response)
    return make_response(jsonify(response),200)


def retrieve_question():
    return

def update_question():
    return

def delete_question():
    return