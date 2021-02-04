import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from datetime import time, datetime, timedelta, date
from enum import Enum
import requests
import get_pictures

list_of_users = []
token = '8c9954383a63ff1f3be3426fc1cf27425d21114ed9f0712d1d8244eb3100ee04df1e8583a284f5391e484'
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
session = requests.Session()
bot = '[club202310522|@public202310522]'

class Weekdays(Enum):
    MON = 0
    TUE = 1
    WEN = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


class lesson:

    def __init__(self, time, room, name):
        self.time = time
        self.room = room
        self.name = name

timetables = {'вторник' : 'https://raw.githubusercontent.com/KristinaKulabuhova/VkBot/master/pictures/Tuesday.jpg',
              'среда' : 'https://raw.githubusercontent.com/KristinaKulabuhova/VkBot/master/pictures/Wednesday.jpg',
              'четверг' : 'https://raw.githubusercontent.com/KristinaKulabuhova/VkBot/master/pictures/Thursday.jpg',
              'пятница' : 'https://raw.githubusercontent.com/KristinaKulabuhova/VkBot/master/pictures/Friday.jpg',
              'суббота' : 'https://raw.githubusercontent.com/KristinaKulabuhova/VkBot/master/pictures/Saturday.jpg'}

lessons=\
            {Weekdays.TUE : 
                    [lesson(time=time(9, 00, 00),  room='УЛК_1 №2.36',    name='Практика на С++'),
                     lesson(time=time(12, 20, 00), room='413 ГК',         name='Гармонический анализ'),
                     lesson(time=time(15, 55, 00), room='НК',             name='Иностранный язык'),
                     lesson(time=time(15, 5, 00),  room='_',              name='Физическая культура')],
             Weekdays.WEN: 
                    [lesson(time=time(9, 00, 00),  room='422 ГК',         name='Диффуренциальные уравнения'),
                     lesson(time=time(10, 45, 00), room='_',              name='Физическая культура'),
                     lesson(time=time(12, 20, 00), room='?',              name='ТиПМС'),
                     lesson(time=time(17, 5, 00),  room='УЛК_2 №418-419', name='Базы данных')],
             Weekdays.THU: 
                    [lesson(time=time(9, 00, 00),  room='202 НК',         name='Гармонический анализ. Лекция'),
                     lesson(time=time(13, 55, 00), room='113 ГК',         name='Дискретные структуры. Лекция')],
             Weekdays.FRI: 
                    [lesson(time=time(9, 00, 00),  room='УЛК_1 №2.36',    name='Практика на С++'),
                     lesson(time=time(13, 55, 00), room='512 ГК',         name='Теория вероятностей'),
                     lesson(time=time(15, 30, 00), room='518 ГК',         name='Дискретные структуры')],
             Weekdays.SUN: 
                    [lesson(time=time(9, 00, 00),  room='_',              name='Дифференциальные уравнения. Лекция'),
                     lesson(time=time(10, 45, 00), room='_',              name='Теория вероятностей. Лекция'),
                     lesson(time=time(12, 20, 00), room='_',              name='ТиПМС. Лекция'),
                     lesson(time=time(13, 55, 00), room='_',              name='Базы данных. Лекция'),
                     lesson(time=time(16, 00, 00), room='_',              name='Введение в анализ данных. Лекция')]}


def get_time_difference(t1, t2):
    current_day = date.today()
    return datetime.combine(current_day, t1) -  datetime.combine(current_day, t2)

def the_nearest_lesson():
    time = datetime.now().time()
    day = Weekdays(datetime.now().weekday())

    min_delta = timedelta.max
    lesson_idx = -1

    for i in range(len(lessons[day])):
        if lessons[day][i].time > time:
            cur_delta = get_time_difference(lessons[day][i].time, time)
            if cur_delta < min_delta:
                min_delta = cur_delta
                lesson_idx = i

    return (lesson_idx, day)
  

def the_nearest_lesson_string():

    lesson_idx, day = the_nearest_lesson()
    
    if lesson_idx == -1:
        return 'На сегодня пары закончились)'

    closest_lesson = lessons[day][lesson_idx]
    return closest_lesson.name + ' в ' + closest_lesson.time.strftime("%H:%M") + '. Аудитория ' + closest_lesson.room

def answer(id, text):
    vk_session.method('messages.send', {'chat_id' : id, 'message' : text, 'random_id' : 0})

def timetable(id, text, keyboard):
    vk_session.method('messages.send', {'chat_id' : id, 'message' : text, 'random_id' : 0, 'keyboard' : keyboard})

def create_menu():
    keyboard = VkKeyboard(one_time=False, inline=False)

    keyboard.add_button(label='Расписание', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(label='Ближайшая пара', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_openlink_button(label='Полезные материалы', link="https://yandex.ru/")
    keyboard = keyboard.get_keyboard()
    return keyboard

def create_keyboard(response):
    keyboard = VkKeyboard(one_time=True)

    if response == 'расписание':

        keyboard.add_button(label='Вторник', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Среда', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Четверг', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Пятница', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Суббота', color=VkKeyboardColor.POSITIVE)

    keyboard = keyboard.get_keyboard()
    return keyboard

def send_message(id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send', {'user_id': id, 'message': message, 'random_id': 0, 'attachment': attachment, 'keyboard': keyboard})

def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            id = event.user_id
            if list_of_users.count(id) == 0:
                list_of_users.append(id)
            response = event.text.lower()
            keyboard_menu = create_menu()
            if event.from_user and not event.from_me:
                if response == 'начать':
                    send_message(id, message='Возможные действия', keyboard=keyboard_menu)
                if response == 'расписание':
                    keyboard = create_keyboard(response)
                    send_message(id, message='Выберите день', keyboard=keyboard)
                elif response == 'ближайшая пара':
                    send_message(id, message=the_nearest_lesson_string(), keyboard=keyboard_menu)
                elif response in timetables.keys():
                    attachment = get_pictures.get(vk_session, session, timetables[response])
                    send_message(id, message=response.capitalize(), attachment=attachment, keyboard=keyboard_menu)


def main_thread_worker():
    while True:
        main()

def notification_thread_worker():
    while True:
        lesson_idx, day = the_nearest_lesson()
        if lesson_idx != -1:
            delta = get_time_difference(lessons[day][lesson_idx].time, datetime.now().time)
            ten_minute_delta = timedelta(minutes=10)

            if delta <= ten_minute_delta:
                    


