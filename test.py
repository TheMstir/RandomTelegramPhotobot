# ждем получения фото
photo_message = await bot.await_next_event(
    types.NewMessage(chat=message.chat.id, content_types=types.ContentType.PHOTO))
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
