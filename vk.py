from typing import Dict, Any, List

import vk_api
from key import main_token


def search_user(name: str, age_from: int, age_to: int, sex: int, city: str):
    # with open('token.txt', 'r') as file_object:
    #     token = file_object.readline().strip()

    version: str = '5.154'

    params = {
        'v': version,
        'count': 1000,
        'is_closed': False,
        'fields': 'city, bdate',
        'q': name,
        'age_from': age_from,
        'age_to': age_to,
        'sex': sex,
        'has_photo': 1,
        'online': 1,
        'hometown': city,
        'sort': 0
            }
    session = vk_api.VkApi(token=main_token)
    result = session.method('users.search', params)['items']
    for item in result:
        dic_user = {}
        if item['is_closed']:
            continue
        # if item['city']['title'].lower() != city.lower():
        #     continue
        params_photo = {
            'owner_id': item['id'],
            'album_id': 'profile',
            'v': version,
            'extended': 1
        }
        photo_user = session.method('photos.get', params_photo)['items']
        sort_photo = sorted(photo_user, key=lambda x: x['likes']['count'], reverse=True)
        dic_user['id'] = item['id']
        dic_user['name'] = f'{item['first_name']} {item['last_name']}'
        #dic_user['last_name'] = item['last_name']
        dic_user['city'] = city
        if item['bdate']:
            dic_user['date_birth'] = item['bdate']
        else:
            dic_user['date_birth'] = None
        list_id_photo = []
        for photo in sort_photo:
            list_id_photo.append(photo['id'])
            if len(list_id_photo) == 3:
                break
        dic_user['photo'] = list_id_photo
        #print(dic_user)
        yield dic_user

