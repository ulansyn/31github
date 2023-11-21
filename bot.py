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


def sender(chat_id, audio_file, value):
    audio = open(f"{audio_file}", 'rb')
    bot.send_audio(chat_id, audio)
    current_time = curr_time()
    print(f'[{current_time}] Аудио отправлено для {chat_id}')
    spoiler_text = value

    formatted_text = f"||{spoiler_text}||"

    bot.send_message(chat_id, formatted_text, parse_mode='MarkdownV2')


def generate_and_send_audio(chat_id):
    current_time = curr_time()
    print(f'[{current_time}] Была вызвана функция для {chat_id}')
    random_number = randint(1, 10000)
    current_time = curr_time()
    print(f'[{current_time}] Выбрано число {random_number} для {chat_id}')

    user_numbers[chat_id] = str(random_number)

    number_str = str(random_number)

    tts = gTTS(text=number_str, lang='de')
    tts.save("output1.mp3")

    sender(chat_id, audio_file="output1.mp3", value=number_str)


def generate_audio_for_time(chat_id='', hour=0, minute=0, language='de'):
    hour = randint(0, 24)
    minute = randint(0, 59)
    if minute < 30:
        time_string = f"Es ist {minute} Minuten nach {hour} Uhr"
    else:
        time_string = f"Es ist {60 - minute} Minuten vor {hour + 1} Uhr"
    hour = "0" + str(hour) if 0 <= hour <= 9 else str(hour)
    minute = "0" + str(minute) if 0 <= minute <= 9 else str(minute)
    user_numbers[chat_id] = str(hour) + ":" + str(minute)

    tts = gTTS(text=time_string, lang=language, slow=False)
    rand = randint(1, 1000000)
    tts.save(f"generated_audio{rand}.mp3")
    print(f"Аудио сгенерировано и сохранено")
    print(str(hour) + ":" + str(minute))
    sender(chat_id, audio_file=f"generated_audio{rand}.mp3", value=str(hour) + ":" + str(minute))


@bot.message_handler(commands=['start'])
def handle_start(message):
    current_time = curr_time()
    print(f'[{current_time}] Была вызвана функция @handle_start для {message.chat.id}')
    chat_id = message.chat.id
    if randint(0, 1) == 1:
        generate_and_send_audio(chat_id)
    else:
        generate_audio_for_time(chat_id=chat_id)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_guess = message.text
    print(user_guess)
    current_number = user_numbers.get(chat_id)
    print(current_number)

    if current_number is not None:
        if user_guess == current_number:
            bot.send_message(chat_id, "Правильно.")
            current_time = curr_time()
            print(f"[{current_time}] Пользователь {chat_id} ответил gравильно.")
            del user_numbers[chat_id]
            if randint(0, 1) == 1:
                generate_and_send_audio(chat_id)
            else:
                generate_audio_for_time(chat_id=chat_id)
        else:
            bot.send_message(chat_id, "Неправильно.")
            current_time = curr_time()
            print(f"[{current_time}] Пользователь {chat_id} ответил неправильно")
            bot.send_audio(chat_id, curr_audio)
    else:
        bot.send_message(chat_id, "Напиши /start.")


bot.polling(none_stop=True)
