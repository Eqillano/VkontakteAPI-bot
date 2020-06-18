import vk_api
from vk_api.bot_longpoll import VkBotLongPoll,VkBotEventType,VkBotMessageEvent
import random

token = '667d414536d5a8259ed6520e8f833d1978dae0b0eff10a916bc6c9dc41d03091253747adf2fd9915affd6'
group_id = '196426922'



class Bot:
    def __init__(self,group_id,token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk,self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            print('получено сообщение')
            try:
                self.on_event(event)
            except Exception as err:
                print(err)

    def on_event(self,event):
        if event.type == VkBotEventType.MESSAGE_NEW:
           print(event.object['text'])
           self.api.messages.send(
           message=event.object['text'],
           random_id=random.randint(0,2 ** 20),
           peer_id = event.object['peer_id'])
        else:
          print('мы пока не умеем с такии работать',event.type)





if __name__ == '__main__':
    bot = Bot(group_id,token)
    bot.run()
