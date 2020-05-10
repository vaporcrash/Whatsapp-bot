from app.config import configurations
from app.exceptions.TelegramErrors import *
from app.bot.bots import QuizMasterBot,PlayerBot,MaestroBot
import multiprocessing as mp
from app.utils.constants import *
# from app.bot.bot_utils import
import queue


def launch_orchestrator():
    maestro = MaestroBot()
    maestro.run()
    return


class Handler:

    player_messages = {READY,PLAYER_ANSWER}
    quiz_master_messages = {PREPARE_BOTS,COMMENCE_QUIZ,SCORE_UPDATE,BROADCAST}

    def __init__(self,db_client):
        self._input_q = queue.Queue()
        self.quizMaster = QuizMasterBot(db_client)
        self.player = PlayerBot(db_client)

        self.masters_only_groups = configurations.master_groups
        self.player_commands = {"/ready","/ans","/score"}
        self.master_commands = {"/commence","/prepare","/forward","/reward","/deduct","/stop_quiz","/rules"}

    def determine_handler(self,msg):
        if self.is_new_participant(msg):
            return
        if self.from_players(msg) and not self.is_new_participant(msg):
            cmd = self.get_command(msg, self.player_commands)
            if cmd == "/ready":
                self.player.handle_ready_message(group_id=self.get_id(msg),group_name = self.get_chat_title(msg))
            elif cmd == "/ans":
                self.player.handle_answer_message(group_id=self.get_id(msg),group_name=self.get_chat_title(msg),
                                                  text=self.get_msg_text(msg,strip_cmd=cmd))
            elif cmd == "/score":
                self.player.handle_score_request(group_id=self.get_id(msg))
        else:
            cmd = self.get_command(msg, self.master_commands)
            if cmd == "/prepare":
                self.quizMaster.time_to_prepare(quiz_name=self.get_msg_text(msg,strip_cmd=cmd))
            elif cmd == "/commence":
                # divide registered groups equally amongst admins
                self.quizMaster.assign_players_to_master()
                # start background orchestrator
                p = mp.Process(target=launch_orchestrator)
                p.start()
            elif cmd == "/reward":
                self.quizMaster.update_score(group_id=self.get_id_from_reply(msg),
                                              score=self.get_msg_text(msg,strip_cmd=cmd),
                                              question_num="0")
            elif cmd == "/stop_quiz":
                self.quizMaster.stop_quiz()



    def get_command(self,msg: str, commands):
        # TODO : re-implement this with a regex operation instead of searching like this
        for cmd in commands:
            index = self.get_msg_text(msg).find(cmd)
            if index == 0:
                return cmd

        raise UnknownCommand("{} command not known".format(msg))


    def is_new_participant(self,msg):
        return "new_chat_participant" in msg["message"]

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



    def get_id_from_reply(self,msg):
        answer = msg["message"]["reply_to_message"]["text"]
        group_id= answer[answer.find("#")+1:answer.find(":")]
        return group_id

    def get_id(self,msg):
        return msg["message"]["chat"]["id"]
