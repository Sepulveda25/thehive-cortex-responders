#!/usr/bin/env python
# encoding: utf-8

from cortexutils.responder import Responder
import telegram

def send(msg, chat_id, token):
	"""
	Send a mensage to a telegram user specified on chatId
	chat_id must be a number!
	"""
	bot = telegram.Bot(token=token)
	bot.sendMessage(chat_id=chat_id, text=msg)
	return;
		

class Telegram(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.User = self.get_param('config.User', '')
        self.Token_Telegram = self.get_param('config.Token_Telegram', '')

    def run(self):
        Responder.run(self)

        title = self.get_param('data.title', None, 'title is missing')
        title = title.encode('utf-8')

        description = self.get_param('data.description', None, 'description is missing')
        description = description.encode('utf-8')

	i = 0

        mail_to = None
        if self.data_type == 'thehive:case':     
		i = 1
             # self.error('recipient address not found in observables')
        elif self.data_type == 'thehive:alert':
		i = 2
             # self.error('recipient address not found in observables')
        else:
            self.error('Invalid dataType')


	send(title, 20, self.Token_Telegram)
        self.report({'message': self.Token_Telegram })

    


    def operations(self, raw):
        return [self.build_operation('AddTagToCase', tag='mail sent')]


if __name__ == '__main__':
    Telegram().run()
