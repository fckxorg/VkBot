import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
from datetime import datetime
import requests
import get_pictures

token = '8c9954383a63ff1f3be3426fc1cf27425d21114ed9f0712d1d8244eb3100ee04df1e8583a284f5391e484'
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
session = requests.Session()


def answer(id, text):
    vk_session.method('messages.send', {'chat_id' : id, 'message' : text, 'random_id' : 0})

def timetable(id, text, keyboard):
    vk_session.method('messages.send', {'chat_id' : id, 'message' : text, 'random_id' : 0, 'keyboard' : keyboard})

def create_keyboard(response):
    keyboard = VkKeyboard(one_time=True)

    if response == 'расписание':

        keyboard.add_button('Вторник', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Среда', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Четверг', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Пятница', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Суббота', color=VkKeyboardColor.POSITIVE)

    #elif response == 'вторник':
    keyboard = keyboard.get_keyboard()
    return keyboard

def send_message(id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send', {'chat_id': id, 'message': message, 'random_id': 0, 'attachment': attachment, 'keyboard': keyboard})

def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            id = event.chat_id
            response = event.text.lower()
            keyboard = create_keyboard(response)
            if event.from_chat and not event.from_me:
                if response == 'расписание':
                    print(response)
                    send_message(id, message='Вот расписание', keyboard=keyboard)
                elif response == 'вторник':
                    print(response)
                    attachment = get_pictures.get(vk_session, session, -202310522, session_api)
                    send_message(id, message='Расписание на вторник', attachment=attachment)

while True:
    main()
