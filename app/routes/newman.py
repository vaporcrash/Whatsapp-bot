from app import app,db
from flask import request as flask_request
from flask import  jsonify,make_response
from app.models.Handler import Handler
import traceback
import logging


logger = logging.getLogger(__name__)


handler = Handler(db)

@app.route("/messenger",methods=["POST"])
def on_receive():
    try:
        token  = flask_request.args.get("token")
        if token != "1135804192:AAEtfVu4MZJuqesF6Wsph6UU0mtmPJZM2hQ":
            return make_response({},405)

        body = flask_request.json
        print(body)
        # send_message(body)
        handler.determine_handler(body)
    except Exception:
        traceback.print_exc()

    finally:
        return make_response(jsonify({}),200)