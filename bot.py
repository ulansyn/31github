from gtts import gTTS
import os
import telebot
from random import randint
from datetime import datetime

BOT_TOKEN = 'MYTOKEN'
bot = telebot.TeleBot(BOT_TOKEN)
user_numbers = {}
curr_audio = ''


def curr_time():
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


def generate_and_send_audio(chat_id):
    current_time = curr_time()
    print(f'[{current_time}] Была вызвана функция для {chat_id}')
    random_number = randint(1, 10000)
    current_time = curr_time()
    print(f'[{current_time}] Выбрано число {random_number} для {chat_id}')

    user_numbers[chat_id] = random_number

    number_str = str(random_number)

    tts = gTTS(text=number_str, lang='de')
    tts.save("output1.mp3")
    curr_audio = "output1.mp3"
    current_time = curr_time()
    print(f'[{current_time}] Аудио сохранено для {chat_id}')

    audio_file = open("output1.mp3", 'rb')
    bot.send_audio(chat_id, audio_file)
    current_time = curr_time()
    print(f'[{current_time}] Аудио отправлено для {chat_id}')
    spoiler_text = random_number

    formatted_text = f"||{spoiler_text}||"

    bot.send_message(chat_id, formatted_text, parse_mode='MarkdownV2')


@bot.message_handler(commands=['start'])
def handle_start(message):
    current_time = curr_time()
    print(f'[{current_time}] Была вызвана функция @handle_start для {message.chat.id}')
    chat_id = message.chat.id
    generate_and_send_audio(chat_id)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_guess = message.text
    try:
        user_guess = int(user_guess)
    except ValueError:
        bot.send_message(chat_id, "Напишите число.")
        return

    current_number = user_numbers.get(chat_id)

    if current_number is not None:
        if user_guess == current_number:
            bot.send_message(chat_id, "Правильно.")
            current_time = curr_time()
            print(f"[{current_time}] Пользователь {chat_id} ответил gравильно.")
            del user_numbers[chat_id]
            generate_and_send_audio(chat_id)
        else:
            bot.send_message(chat_id, "Неправильно.")
            current_time = curr_time()
            print(f"[{current_time}] Пользователь {chat_id} ответил неправильно")
            bot.send_audio(chat_id, curr_audio)
    else:
        bot.send_message(chat_id, "Напиши /start.")


bot.polling(none_stop=True)
