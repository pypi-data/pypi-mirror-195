from app.models.bot import Bot
from app.utils.print import print_message

class Chat:
    def __init__(self, key):
        self.bot = Bot(key)
        self.chat = []

    def log_message(self, role, content):
        message = {
            "role": role,
            "content": content
        }

        self.chat.append(message)

        if role != "user":
            print_message(message)


    def send_message(self, prompt):
        self.log_message("user", prompt)

        reply = self.bot.request(self.chat)

        if reply:
            self.log_message("assistant", reply)
            return reply

