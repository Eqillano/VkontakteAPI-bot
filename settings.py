INTENTS = [
    {
        'name': 'дата проведения',
        'tokens':('когда', 'какая', 'дата', 'во сколько'),
        'scenario': None,
        'answer': 'Конференция пройдет 12 июня, регистрация начнется в 10 утра'
    },
    {
        'name': 'приветствие',
        'tokens': ('привет'),
        'scenario': None,
        'answer': 'Привет, {name}! У меня ты можешь узнать информацию о конференции и зарегестрироваться на нее'
    },
    {
        'name': 'место проведения',
        'tokens': ('где','место', 'будет', 'адрес', 'локация'),
        'scenario': None,
        'answer': 'Конференция пройдет в павильоне 18Г в Экспоцентре'
    },
    {
        'name': 'регистрация',
        'tokens': ('регистр', 'добав', 'вкл'),
        'scenario': None,
        'answer': 'Использовать ваше имя Вконтакте или выбрать другое?'
    },
    {
        'name': 'имя в вк',
        'tokens': ('да ', 'использовать', 'это'),
        'scenario': 'registration',
        'first_step': 'step_2',
        'answer': None
    },
    {
        'name': 'другое имя',
        'tokens': ('нет', 'не ', 'другое'),
        'scenario': 'registration',
        'first_step': 'step_1',
        'answer': None
    },
]

SCENARIOS = {
    'registration': {
        'steps': {
            'step_1': {
                'text': 'Чтобы зарегистрироваться введите свое имя. Оно будет написано на бейджике',
                'failure_text': 'Имя не должно содержать цифр и должно состоять из 3-30 знаков, включая дефис',
                'handler': 'handler_name',
                'next_step': 'step_2',
            },
            'step_2': {
                'text': 'Добавьте свой E-mail.  На него мы пришем письмо с подтверждением регистрации',
                'failure_text': 'E-mail содержит некорректые символы. Пример E-mail: example@example.com',
                'handler': 'handler_email',
                'next_step': 'step_3',
            },
            'step_3': {
                'text': 'Спасибо за регистрацию, {name}! На почту {mail} выслано приглашение, будем ждать вас!',
                'failure_text': None,
                'handlers': None,
                'next_step': None
            },
        }
    }
}


DEFAULT_MESSAGE = "Я пока не умею обрабатывать такие вопросы. У меня ты можешь узнать когда и где пройдет конференция"


DB_CONFIG = dict(
provider='postgres',user='postgres',password='qwerty67',host='localhost',database='vk_chat_bot'
)
