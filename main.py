import asyncio
import logging
import os
import random
import time

from aiogram.utils.formatting import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder

import setting
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import cv # это функции комиксирования
import vk_api_funk
import tales

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=setting.api_token, parse_mode='HTML')
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))  # Команда для инициации со стороны пользователя
async def cmd_start(message: types.Message):
    # кнопки которые появляются со стартом
    kb = [
        [
            types.KeyboardButton(text="случайный комикс"),
            types.KeyboardButton(text="другое")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=""
    )

    await message.answer("Гав-гав! Привет!🐶"
                         "\nЯ Песмит-бот🦴, выдаю случайный комикс про себя по запросу /comix.🌭"
                         "\nПонемногу я обрастаю разными функциями =, например /story"
                         "\nУ меня есть режим эхо и позже появятся еще функции, узнай их по запросу /help",
                         reply_markup=keyboard)


async def download_photo(photo: types.PhotoSize):
    file_path = os.path.join('/tmp', f"{photo.file_unique_id}.jpg")
    await bot.download(photo.file_id, file_path)
    return file_path


@dp.message(Command('photo'))
async def send_photo(message: types.Message, bot:Bot):
    await bot.download(
        message.photo[-1],
        destination=f"/tmp/{message.photo[-1].file_id}.jpg"
        )


@dp.message(Command("comix"))
async def send_random_comix(message: types.Message, bot:Bot):
    # file_ids = [] # если по несколько отправлять (пока не вижу необходимости)
    image_from_url = types.URLInputFile(vk_api_funk.get_random_comix(), bot)

    # простейший режим логирования для анализа
    with open('log.txt', 'a', encoding='utf-8') as l:
        l.write(f'-> Пользователь {message.chat.username} запросил комикс и получил {image_from_url}\n')

    kb = [
        [
            types.KeyboardButton(text="случайный комикс"),
            types.KeyboardButton(text="другое"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=""
    )
    # builder = InlineKeyboardBuilder()
    # builder.add(types.InlineKeyboardButton(
    #     text="ДА 🐶🦴",
    #     callback_data="comix")
    # )

    # варианты ответов
    answer = ('Вот такой', 'У меня есть вот этот', 'Смотри какой ещё есть', 'Это мне нравится',
              'Получите - распишитесь', 'Опять работа? Знаю-знаю, я сам предполагаю', "Гав-гав!",
              '🐶', '🐕‍🦺', 'Вот бы мне косточку за скорость!', 'Я быстрый пёс', 'Хороший мальчик выполнил задание!')

    await message.answer_photo(
        image_from_url,
        caption=random.choice(answer),
    )
    await message.answer('Хочешь ещё? /comix 🐶🦴', reply_markup=keyboard)


@dp.message(Command("story"))
async def story_mode(message: types.Message):
    """Хэндлер запрашивает у функции какую-нибудь генерированую историю и отправляет пользователю"""
    await message.answer(tales.read_and_send())
    time.sleep(30) # время на чтение
    await help_menu(message) #возвращаем меню


@dp.message(Command("help"))
async def help_menu(message: types.Message):
    """Меню"""
    await message.answer('МЕНЮ:\nТут кратко описаны функции:'
                         '\n/comix - отправит вам случайный выпуск комикса про маленького рыжего пса'
                         '\n/story - истории о песиках, сгенерированные нейросетью'
                         '\n/help - это меню')
    #  '\n/photo - небольшой обработчик ваших картинок и фотографий'


@dp.message(lambda message: message.text == "другое")
async def help_button(message: types.Message):
    """перенаправляет в меню"""
    await help_menu(message)


@dp.message(lambda message: message.text == "случайный комикс")
async def with_puree(message: types.Message):
    """кнопка случайного комикса"""
    await send_random_comix(message, bot)


@dp.message() # Эхо событие, которое запускается
# в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message): #Создаём функцию с простой задачей
    # — отправить обратно тот же текст, что ввёл пользователь.
    await message.answer(f'Все говорят {message.text}, а ты купи слона')

# Пока нерабочая всплывающая кнопка
# @dp.callback_query(Command("comix"))
# async def send_random_value(callback: types.CallbackQuery):
#     print('мы тут')
#     await send_random_comix(callback.message, bot)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())