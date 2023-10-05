from key import token
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk import search_user

vk_session = vk_api.VkApi(token=token)
longpoll: VkLongPoll = VkLongPoll(vk_session)


def send_mes(user_id, text, keyboard=None):
    param = {
        'user_id': user_id,
        'message': text,
        'random_id': 0
    }
    if keyboard != None:
        param['keyboard'] = keyboard.get_keyboard()
    vk_session.method('messages.send', param)


def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            mes = event.text.lower()
            id = event.user_id
            print(mes)
            if mes in ['начать', 'start']:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Да')
                keyboard.add_button('Нет')
                keyboard.add_button('Помощь')
                send_mes(id, 'Привет! Это бот Love Bot. Запустить поиск пары?', keyboard)
                second_main(id)
            else:
                send_mes(id, 'Как дела? Хотите просто поболтать?')


def second_main(id):
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            mes = event.text.lower()
            #id = event.user_id
            if mes == 'да':
                search_love(id)
            if mes == 'нет':
                send_mes(id, 'Очень жаль. Досвидания.')
                main()
            if mes == 'Помощь':
                send_mes(id, 'Пока в разработке')
            else:
                main()


def search_love(id):
    name: str = None
    city: str = None
    age: int = None
    sex: int = None

    send_mes(id, 'Введите Имя')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            mes = event.text.lower()
            if name == None:
                name = mes
                send_mes(id, 'Введите Город')
                continue
            if name != None and city == None:
                city = mes
                send_mes(id, 'Введите Возраст')
                continue
            if name != None and city != None and age == None:
                age = int(mes) # Сделать обработчик
                send_mes(id, 'Введите Пол (Муж/Жен)')
                continue
            if name != None and city != None and age != None and sex == None:
                if mes == 'муж':
                    sex = 2
                elif mes == 'жен':
                    sex = 1
                else:
                    sex = 0
                if name != None and city != None and age != None and sex != None:
                    # item = iter(search_user(name, age, sex, city))
                    # user = next(item)
                    # send_mes(id, f'Первая пара {user["first_name"]}')
                    view_user(id, name, age, sex, city)



def view_user(id, name, age, sex, city):
    #print(name, age, sex, city)
    item = iter(search_user(name, age, sex, city))
    user = next(item)
    # print(user)
    send_mes(id, f'Первая пара {user["first_name"]}, {user["last_name"]}')
    # for event in longpoll.listen():
    #     if event.type == VkEventType.MESSAGE_NEW and event.to_me:



if __name__ == '__main__':
    main()
    # item = iter(search_user('роман', 25, 2, 'москва'))
    # print(next(item)["first_name"])
    # print(next(item))
