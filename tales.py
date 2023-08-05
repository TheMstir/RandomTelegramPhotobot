import random
from pathlib import Path


def read_and_send():
    """Считает колличество файлов в папке с 'историями', случайно выбирает
    один из файлов и отправляет его текст пользователю"""
    folder = Path('tales')
    if folder.is_dir():
        folder_count = len([1 for file in folder.iterdir()])
        print(folder_count)

    dice = random.randint(1, folder_count - 1)
    with open(f'tales/{dice}.txt', 'r', encoding='utf-8') as tale:
        history = tale.read()
        return history