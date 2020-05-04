from app import app,db
import json
from flask import request,jsonify,make_response
from app.models import NewmanBot
import logging
import requests

murl = "https://api.telegram.org/bot1135804192:AAEtfVu4MZJuqesF6Wsph6UU0mtmPJZM2hQ/sendMessage"

logger = logging.getLogger(__name__)

bot = NewmanBot()

def send_message(req):
    chat_id = req["message"]["chat"]["id"]
    rep = {"chat_id" : chat_id, "text" : "Bella Ciao, Bella Ciao, Bella Ciao Ciao Caio!"}

    res = requests.post(murl,json=rep)
    print(res.status_code)




@app.route("/",methods=["POST"])
def on_receive():
    body = request.json
    print(body)
    logger.error("recieved")
    # send_message(body)
    return make_response(jsonify({}),200)