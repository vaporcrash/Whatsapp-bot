

class TelegramSendError(Exception):
    pass

class TelegramBadMessage(Exception):
    pass


class UnknownTelegramGroup(Exception):
    pass

class UnknownCommand(Exception):
    pass