from app.config import configurations
from app.exceptions.TelegramErrors import *
from app.bot.bots import QuizMasterBot,PlayerBot
# from app.bot.bot_utils import
import queue


class Handler:

    def __init__(self,db_client):
        self._input_q = queue.Queue()
        self.quizMaster = QuizMasterBot(db_client)
        self.player = PlayerBot(db_client)

        self.masters_only_groups = configurations.master_groups
        self.player_commands = {"/ready"}
        self.master_commands = {"/commence","/prepare"}

    def launch_orchestrator(self, quiz_name):
        return


    def determine_handler(self,msg):
        if self.from_players(msg):
            cmd = self.get_command(msg, self.player_commands)
            if cmd == "/ready":
                self.player.handle_ready_message(group_id=self.get_id(msg))
        else:
            cmd = self.get_command(msg, self.master_commands)
            if cmd == "/prepare":
                self.quizMaster.time_to_prepare(quiz_name=self.get_msg_text(msg,strip_cmd=cmd))
            if cmd == "/commence":
                self.launch_orchestrator(quiz_name=self.get_msg_text(msg,strip_cmd=cmd))



    def get_command(self,msg: str, commands):
        for cmd in commands:
            index = self.get_msg_text(msg).find(cmd)
            if index == 0:
                return cmd

        raise UnknownCommand("{} command not known".format(msg))

    def from_group(self,msg):
        return msg["message"]["chat"]["type"] == "group"

    def from_players(self,msg):
        return self.from_group(msg) and self.get_chat_title(msg) not in self.masters_only_groups

    def get_chat_title(self,msg):
        return msg["message"]["chat"]["title"]

    def get_msg_text(self,msg,**kwargs):

        if kwargs and "strip_cmd" in kwargs:
            cmd =kwargs["strip_cmd"]
            ind = msg["message"]["text"].find(cmd)
            return msg["message"]["text"][ind+len(cmd)+1:]

        return msg["message"]["text"]

    def get_id(self,msg):
        return msg["message"]["chat"]["id"]
