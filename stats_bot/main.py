import telebot
import threading
import time
import os
from STATweight_add_del import adder, remover, last_value, get_all_values
import matplotlib
from STATweight import send_graph, NAME

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

START = 77  # kg
GOAL = 67  # kg


def countofvals():
    cnt = 0
    with open('МОЙВЕС.txt', 'r') as file:
        for line in file:
            if is_valid_number(line):
                cnt += 1
    return cnt


def is_valid_number(text):
    text = text.replace(',', '.')
    try:
        number = float(text)
        if 60 <= number <= 85:
            return True
    except ValueError:
        pass
    return False


def to_valid_number(text):
    text = text.replace(',', '.')
    return text


def info(n):
    # ostatok
    x = float(n) - GOAL  # kg
    completed = int((x / 10) * 100)  # %
    s = f"""Похудел на {START - float(n):.2f} кг
Осталось скинуть еще {x:.2f} кг
Выполнено {100 - completed}% от плана
(При норме {int(countofvals() * 100 / 244)}%)
    """
    return s


TOKEN = '6667117025:AAGgB2dcMpgmLVIkq9SJjz0pD_AfDf6EbAs'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот-эхо. Пришлите мне сообщение, и я повторю его.")


@bot.message_handler(func=lambda message: is_valid_number(message.text))
def handle_valid_number(message):
    adder(to_valid_number(message.text))
    bot.send_message(message.chat.id, f'Данные записаны!')
    bot.send_message(message.chat.id, info(message.text))
    with open('defgraph.txt', 'r') as file:
        content = file.read()
        if '1' in content:
            handle_valid_number(message)


@bot.message_handler(commands=['del'])
def handle_valid_number(message):
    remover()
    bot.send_message(message.chat.id, f'Последнее значение удалено!')
    with open('defgraph.txt', 'r') as file:
        content = file.read()
        if '1' in content:
            handle_valid_number(message)


@bot.message_handler(commands=['last'])
def handle_valid_number(message):
    bot.send_message(message.chat.id, f'Last value {last_value()}')


@bot.message_handler(commands=['switchgraph'])
def handle_valid_number(message):
    isTrue = True
    with open('defgraph.txt', 'r+') as file:
        content = file.read()
        if '1' in content:
            content = content.replace('1', '0')
            isTrue = False
        elif '0' in content:
            content = content.replace('0', '1')
            isTrue = True
        file.seek(0)
        file.write(content)
        file.truncate()

    bot.send_message(message.chat.id, f'{"Был включен график" if isTrue else "График был выключен"}')


@bot.message_handler(commands=['getvalues'])
def handle_valid_number(message):
    bot.send_message(message.chat.id, f'{get_all_values()}')


@bot.message_handler(commands=['info'])
def handle_valid_number(message):
    bot.send_message(message.chat.id, f'{info(last_value())}')


@bot.message_handler(commands=['graph'])
def handle_valid_number(message):
    # Запускаем функцию send_graph в отдельном потоке
    threading.Thread(target=send_graph_and_send_photo, args=(message.chat.id,)).start()


# Функция для генерации и отправки графика
def send_graph_and_send_photo(chat_id):
    send_graph()

    with open(f'{NAME}.jpg', 'rb') as photo:
        bot.send_photo(chat_id, photo)

    # Ожидание завершения отправки фотографии
    while threading.active_count() > 1:  # Подсчет активных потоков, идентифицирующихся как 1, где 1 - основной поток
        time.sleep(1)

    # После завершения отправки фотографии можно удалить файл
    try:
        os.remove(f'{NAME}.jpg')
    except PermissionError:
        print(f"Файл '{NAME}.jpg' занят другим процессом и не может быть удален.")

    plt.clf()


bot.polling(none_stop=True)
