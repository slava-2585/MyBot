from key import token
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk import search_user

vk_session = vk_api.VkApi(token=token)
longpoll: VkLongPoll = VkLongPoll(vk_session)


def send_mes(user_id, text, keyboard=None, attachment=None):
    param = {
        'user_id': user_id,
        'message': text,
        'random_id': 0
    }
    if keyboard != None:
        param['keyboard'] = keyboard.get_keyboard()
    if attachment != None:
        param['attachment'] = attachment
    vk_session.method('messages.send', param)


def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            mes = event.text.lower()
            if mes in ['начать', 'start']:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Да')
                keyboard.add_button('Нет')
                keyboard.add_button('Помощь')
                send_mes(event.user_id, 'Привет! Это бот Love Bot. Запустить поиск пары?', keyboard)
                second_main()
            else:
                send_mes(event.user_id, 'Как дела? Хотите просто поболтать?')


def second_main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            mes = event.text.lower()
            if mes == 'да':
                send_mes(event.user_id, 'Введите Имя')
                search_love()
            if mes == 'нет':
                send_mes(event.user_id, 'Очень жаль. Досвидания.')
                main()
            if mes == 'Помощь':
                send_mes(event.user_id, 'Пока в разработке')
            else:
                main()


def search_love():
    name: str = None
    city: str = None
    age: str = None
    sex: int = None
    age_from: int
    age_to: int

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            id = event.user_id
            mes = event.text.lower()
            if name == None:
                name = mes
                send_mes(event.user_id, 'Введите Город')
                continue
            if name != None and city == None:
                city = mes
                send_mes(event.user_id, 'Введите Возраст')
                continue
            if name != None and city != None and age == None:
                age = mes  # Сделать обработчик
                try:
                    age_from, age_to = age.split("-")
                except ValueError:
                    send_mes(event.user_id, 'Неправильно введен возраст, введите заново)')
                    age = None
                    continue
                try:
                    age_from = int(age_from)
                except ValueError:
                    send_mes(event.user_id, 'Неправильно введен возраст, введите заново)')
                    age = None
                    continue
                try:
                    age_to = int(age_to)
                except ValueError:
                    send_mes(event.user_id, 'Неправильно введен возраст, введите заново)')
                    age = None
                    continue

                send_mes(event.user_id, 'Введите Пол (Муж/Жен)')
            if name != None and city != None and age != None and sex == None:
                if mes == 'муж':
                    sex = 2
                elif mes == 'жен':
                    sex = 1
                else:
                    sex = 0

            if name != None and city != None and age != None and sex != None:
                candidate = iter(search_user(name, age_from, age_to, sex, city))
                view_user(candidate)


def view_user(candidate):
    keyboard1 = VkKeyboard()
    keyboard1.add_button('Лайк')
    keyboard1.add_button('Дизлайк')
    keyboard1.add_line()
    keyboard1.add_button('Дальше')
    keyboard1.add_button('Остановить')
    for event in longpoll.listen():
        attachment: list = []
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                item = next(candidate)
            except StopIteration:
                send_mes(event.user_id, 'Ничего не найдено или список закончился. Приходите снова.')
                main()
            mes = event.text.lower()
            if mes == 'лайк':
                pass
            elif mes == 'дизлайк':
                pass
            elif mes == 'дальше':
                try:
                    item = next(candidate)
                except StopIteration:
                    send_mes(event.user_id, 'Пока все. Будем рады Вас видеть снова.')
            elif mes == 'остановить':
                send_mes(event.user_id, 'Пока. Будем рады видеть Вас снова.')
                main()
            print(attachment)
            send_mes(event.user_id, f'{item['name']} День рождения:{item['date_birth']} Город: {item['city']})', keyboard1)
            for i in range(len(item['photo'])):
                send_mes(event.user_id, f'Фото {str(i + 1)}', keyboard1, f'photo{item['id']}_{item['photo'][i]}')


if __name__ == '__main__':
    main()
    # item = iter(search_user('роман', 25, 2, 'москва'))
    # print(next(item)["first_name"])
    # print(next(item))
