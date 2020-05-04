from app.exceptions import TelegramSendError
from app.config import configurations
from requests import Session
import logging
from functools import partial


logger = logging.getLogger(__name__)

class NewmanBot:

    def __init__(self):
        self.url = configurations.telegram_url
        self.max_retries = 3
        self.session = Session()



    def send_message(self,destination,body):
        message = {
            "chat_id" : destination,
            "text" : body
        }

        for i in range(self.max_retries):
            try:
                response = self.session.post(self.url,json=message,timeout=30)
                if response.status_code == 200:
                    return response.json()
                else:
                    raise TelegramSendError("Dest : {} , Status : {} , Body : {}".format(destination,response.status_code,response.content))
            except TimeoutError:
                logging.error("Message to {} failed. retry {}".format(destination,(i+1)))
                i+=1

        raise TelegramSendError("Dest : {}  Timeout after {} tries!!! ".format(destination,self.max_retries))


    def broadcast_message(self,body):
        group_ids = []
        f = partial(self.send_message,body=body)
        map(f,group_ids)
