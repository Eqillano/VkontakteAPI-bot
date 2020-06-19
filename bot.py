import vk_api
import logging
from vk_api.bot_longpoll import VkBotLongPoll,VkBotEventType,VkBotMessageEvent
import random
import settings
import handlers

token = '667d414536d5a8259ed6520e8f833d1978dae0b0eff10a916bc6c9dc41d03091253747adf2fd9915affd6'
group_id = '196426922'

log = logging.getLogger('bot')

def configure_logging():
    #log = logging.getLogger('bot')
    stream_handler = logging.StreamHandler()
    #stream_handler.setFormatter(logging.Formatter())
    file_handler = logging.FileHandler('bot.log')
    log.addHandler(stream_handler)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)


class UserState:
    def __init__(self,scenario_name,step_name,context=None):
        self.scenario_name = scenario_name
        self.step_name = step_name
        self.context = context or {}

class Bot:
    """
    Echo bot для vk.com
    """
    def __init__(self,group_id,token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk,self.group_id)
        self.api = self.vk.get_api()
        self.user_states = dict()

    def run(self):
        """
        запуск бота
        """
        for event in self.long_poller.listen():
            print('получено сообщение')
            try:
                self.on_event(event)
            except Exception:
                log.exception('ошибка в обработке события')

    def on_event(self,event):
        """
        отправляет сообщение назад если сооб не текствое"""
        if event.type != VkBotEventType.MESSAGE_NEW:
           log.info('мы пока не умеем с таким работать %s',event.type)
           return

        user_id = event.object.peer_id
        text = event.objects.text
        if user_id in self.user_states:
           text_to_send = self.continue_scenario(user_id,text=text)
              # retry current step
        else:
           # search intent
           for intent in settings.INTENTS:
               if any(token in text for token in intent['token']):
                  # run intent
                  if intent['answer']:
                     text_to_send = intent['answer']
                  else:
                     self.start_scenario(user_id,intent['scenario'])
                  break
           else:
               text_to_send = settings.DEFAULT_ANSWER

          self.api.messages.send(
          message=event.object['text'],
          random_id=random.randint(0,2 ** 20),
          peer_id = user_id)
       else:


   def start_scenario(self,user_id,scenario_name):
       scenario = settings.SCENARIOS[scenario_name]
       first_step = scenario['first_step']
       step = scenario['steps'][first_step]
       text_to_send = step['text']
       self.user_states[user_id] = UserState(scenario_name=scenario_name,step_name=first_step)
       return text_to_send





   def continue_scenario(self,user_id,text):
       state = self.user_states[user_id]
          # continue scenario
       steps = settings.SCENARIOS[state.scenario_name]['steps']
       step = steps[state.step_name]
       handler = getattr(handlers,step['handler'])
       if handler(text=text,context=state_context):
             # next step
          next_step = steps[step['next_step']]
          text_to_send = next_step['text'].format(**state_context)
          if next_step['next_step']:
                # switch to next step
             state.step_name = next_step['next_step']
          else:
                # finish scenario
             self.user_states.pop(user_id)
        else:
            # retry current step
            text_to_send = step['failure_text'].format(**state_context)


        return text_to_send




if __name__ == '__main__':
    configure_logging()
    bot = Bot(group_id,token)
    bot.run()
