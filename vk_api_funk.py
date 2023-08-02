import vk_api
import random
import setting


def get_random_comix():
    """Заходит под админом группы песеля, изучает альбом, расчитывает колличество картинок и возвращает одну.
     На случай возможных поломок api есть заглушка 'фотографий нет' """
    vk_session = vk_api.VkApi(token=setting.vk_token)
    vk = vk_session.get_api()

    owner_id = -188854174 # отрицательный id группы
    album_id = 266952866
    photos = vk.photos.get(owner_id=owner_id, album_id=album_id)

    if photos['count'] > 0:
        photo = random.choice(photos['items'])
        photo_url = photo['sizes'][-1]['url'] # получаем url фото максимального размера
        print(photo_url)
    else:
        photo_url = 'вставить сюда адрес куропатки'

        with open('log.txt', 'a', encoding='utf-8') as l:
            l.write(f'-> В альбоме нет фотографий, что-то сломалось!')

        print('В альбоме нет фотографий')

    return photo_url