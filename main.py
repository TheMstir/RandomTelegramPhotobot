import asyncio
import logging
import os

import setting
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import cv # это функции комиксирования
import vk_api_funk

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
            types.KeyboardButton(text="иные функции")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=""
    )

    await message.answer("Гав-гав! Привет!🐶"
                         "\nЯ Песмит-бот🦴, выдаю случайный комикс про себя по запросу /comix.🌭"
                         "\nУ меня есть режим эхо и позже появятся еще функции, узнай их по запросу /help",
                         reply_markup=keyboard)


async def download_photo(photo: types.PhotoSize):
    file_path = os.path.join('/tmp', f"{photo.file_unique_id}.jpg")
    await bot.download_file_by_id(photo.file_id, file_path)
    return file_path


@dp.message(Command('photo'))
async def send_photo(message: types.Message, bot:Bot):
    await message.answer("Отправь мне фотографию, а я верну ее отведенным контуром")
    # ждем получения фото
    photo_message = await bot.await_next_event(types.NewMessage(chat=message.chat.id, content_types=types.ContentType.PHOTO))
    # скачиваем фото

    file_path = await download_photo(photo_message.photo[-1])
    # отправляем пользователю сообщение с фото
    with open(file_path, 'rb') as photo_file:
        input_file = types.InputFile(photo_file)
        await message.answer_photo(input_file)
    # удаляем файл
    os.remove(file_path)

    #
    # result = await message.answer_photo(
    #     image_from_pc,
    #     caption="Изображение из файла на компьютере"
    # )
    # await message.answer("Вот результат:\n" + "\n", photo_message)


@dp.message(Command("comix"))
async def send_random_comix(message: types.Message, bot:Bot):
    file_ids = [] # если по несколько отправлять (пока не вижу необходимости)
    image_from_url = types.URLInputFile(vk_api_funk.get_random_comix(), bot)

    # простейший режим логирования для анализа
    with open('log.txt', 'a', encoding='utf-8') as l:
        l.write(f'-> Пользователь {message.chat.username} запросил комикс и получил {image_from_url}\n')

    result = await message.answer_photo(
        image_from_url,
        caption="Смотри какой, хочешь еще? жми сюда /comix"
    )
    file_ids.append(result.photo[-1].file_id)


@dp.message(F.text.startswith("случайный комикс"))
async def with_puree(message: types.Message):
    """кнопка случайного комикса"""
    await send_random_comix(message, bot)


@dp.message() # новое событие, которое запускается
# в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message): #Создаём функцию с простой задачей
    # — отправить обратно тот же текст, что ввёл пользователь.
    await message.answer(f'Все говорят {message.text}, а ты купи слона')


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())





# import asyncio
#
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import InputFile, URLInputFile
#
# import setting
# import requests
#
# token = setting.api_token
#
# #необходимо инициализировать объекты bot и Dispatcher,
# # передав первому наш токен. Если их не инициализировать,
# # то код не будет работать.
#
# bot = Bot(token=token, parse_mode="HTML")
# dp = Dispatcher(bot)
#
# @dp.message_handler(commands=['start']) # Команда для инициации со стороны пользователя
# async def send_welcome(message: types.Message):
#     # для асинхронности используется AWAIT
#     await message.reply("Привет!\nЯ Псина-комикс-бот\nОтправь мне любое сообщение, "
#                        "а я тебе обязательно отвечу.")
#
#
# # @dp.message_handler() # новое событие, которое запускается
# # # в ответ на любой текст, введённый пользователем.
# # async def echo(message: types.Message): #Создаём функцию с простой задачей
# #     # — отправить обратно тот же текст, что ввёл пользователь.
# #     await message.answer(message.text)
#
#
# @dp.message_handler(commands=['g'])
# async def send_comix(message: types.Message):
#     file_ids = []
#
#     image_from_url = URLInputFile("https://sun9-30.userapi.com/impg/ff5z_HA2KGSeaPXuqFZPhvk-Wi4UCLNHCwBhYA/FWmN1Sqw-Sw.jpg?size=960x1280&quality=95&sign=8b769aa9e946bf9f959d28abd3a8dbe8&type=album")
#     result = await message.answer_photo(
#         image_from_url,
#         caption="Изображение по ссылке"
#     )
#     file_ids.append(result.photo[-1].file_id)
#     await message.answer("Отправленные файлы:\n" + "\n".join(file_ids))
#
#
# @dp.message_handler(commands=['d'])
# async def send_comix(message: types.Message):
#     await message.reply("Hello, <b>world</b>!", parse_mode="HTML")
#
#
#
# if __name__ == '__main__':
#     asyncio.run()