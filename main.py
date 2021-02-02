import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token = '8c9954383a63ff1f3be3426fc1cf27425d21114ed9f0712d1d8244eb3100ee04df1e8583a284f5391e484')
longpoll = VkLongPoll(vk_session)

def answer(id, text):
    vk_session.method('messages.send', {'chat_id' : id, 'message' : text, 'random_id' : 0})

def timetable(id, text, keyboard):
    vk_session.method('messages.send', {'chat_id' : id, 'message' : text, 'random_id' : 0, 'keyboard' : keyboard})


def get_but(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }

keyboard0 = {
    "one_time": False,
    "buttons": [
        [get_but('Расписание', 'positive')],
        [get_but('Ближайщая пара', 'positive')]
    ]
}

keyboard0 = json.dumps(keyboard0, ensure_ascii = False).encode('utf-8')
keyboard0 = str(keyboard0.decode('utf-8'))

keyboard1 = {
    "one_time": True,
    "buttons": [
        [get_but('Вторник', 'positive')],
        [get_but('Среда', 'positive')],
        [get_but('Четверг', 'positive')],
        [get_but('Пятница', 'positive')],
        [get_but('Суббота', 'positive')]
    ]
  }
keyboard1 = json.dumps(keyboard1, ensure_ascii = False).encode('utf-8')
keyboard1 = str(keyboard1.decode('utf-8'))

def main():
    msg = 'Возможные действия'
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            id = event.chat_id
            timetable(id, msg, keyboard0)
            if event.to_me or event.from_me:
                if event.from_chat:

                    msg = event.text.lower()

                    if msg == 'расписание':
                        timetable(id, msg, keyboard1)

while True:
    main()
