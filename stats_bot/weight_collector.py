import telebot
from telebot import types
from datetime import datetime, timedelta
import json
import time
import threading

# Замените 'YOUR_BOT_TOKEN' на ваш токен
TOKEN = '6382702942:AAHabjLr37xRqObXDkIq60ZTFQQapYkBtqs'

bot = telebot.TeleBot(TOKEN)
bot_lock = threading.Lock()
ACTIVE_DATE_FILE = 'active_date.txt'
WEIGHTS_FILE = 'weights.json'


def read_active_date():
    try:
        with open(ACTIVE_DATE_FILE, 'r') as file:
            active_date_str = file.read().strip()
            active_date = datetime.strptime(active_date_str, "%Y-%m-%d")
            return active_date
    except FileNotFoundError:
        with open(ACTIVE_DATE_FILE, 'w') as file:
            active_date = datetime.now()
            file.write(active_date.strftime("%Y-%m-%d"))
            return active_date


def write_active_date(active_date):
    with open(ACTIVE_DATE_FILE, 'w') as file:
        file.write(active_date.strftime("%Y-%m-%d"))


def delete_weight_by_index(date, index):
    weights_data = read_weights()
    date_str = date.strftime("%Y-%m-%d")

    if date_str in weights_data:
        weights = weights_data[date_str]

        if 0 <= index < len(weights):
            deleted_weight = weights.pop(index)
            write_weights(weights_data)
            return deleted_weight

    return None


def read_weights():
    try:
        with open(WEIGHTS_FILE, 'r') as file:
            weights_data = json.load(file)
            return weights_data
    except FileNotFoundError:
        return {}


def write_weights(weights_data):
    with open(WEIGHTS_FILE, 'w') as file:
        json.dump(weights_data, file, indent=4)


@bot.message_handler(commands=['start'])
def start(message):
    active_date = read_active_date()
    send_date_keyboard(message, active_date)
    send_weights_for_date(message.chat.id, active_date)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    current_date = read_active_date()

    if call.data == 'prev_day':
        new_date = current_date - timedelta(days=1)
    elif call.data == 'next_day':
        new_date = current_date + timedelta(days=1)
    elif call.data == 'choose_date':
        bot.send_message(call.message.chat.id, "Пожалуйста, введите дату в формате YYYY-MM-DD:")
        return
    else:
        return

    try:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Сбор данных на {}'.format(new_date.strftime("%d.%m.%Y")),
                              reply_markup=create_date_keyboard(new_date))

        write_active_date(new_date)
        send_weights_for_date(call.message.chat.id, new_date)
    except telebot.apihelper.ApiTelegramException as e:
        pass


@bot.message_handler(commands=['delete_weight'])
def delete_weight_command(message):
    try:
        index = int(message.text.split()[1])
        active_date = read_active_date()
        deleted_weight = delete_weight_by_index(active_date, index - 1)

        if deleted_weight is not None:
            bot.send_message(message.chat.id, f"Вес {deleted_weight} удален.")
            send_weights_for_date(message.chat.id, active_date)
        else:
            bot.send_message(message.chat.id, "Неверный индекс")
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Укажите корректный индекс")


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        weight = float(message.text)
        active_date = read_active_date()

        weights_data = read_weights()
        weights_data.setdefault(active_date.strftime("%Y-%m-%d"), []).append(weight)
        write_weights(weights_data)

        send_weights_for_date(message.chat.id, active_date)
    except ValueError:
        try:
            chosen_date = datetime.strptime(message.text, "%Y-%m-%d")
            write_active_date(chosen_date)
            send_date_keyboard(message, chosen_date)
            send_weights_for_date(message.chat.id, chosen_date)
        except ValueError:
            bot.send_message(message.chat.id, "Введите корректное число или дату в формате YYYY-MM-DD.")


def send_date_keyboard(message, selected_date):
    date_keyboard = create_date_keyboard(selected_date)

    bot.send_message(message.chat.id,
                     'Сбор данных на {}'.format(selected_date.strftime("%d.%m.%Y")),
                     reply_markup=date_keyboard)


def send_weights_for_date(chat_id, date):
    print(2)
    weights_data = read_weights()
    weights = weights_data.get(date.strftime("%Y-%m-%d"), [])

    if weights:
        print(1)
        weight_message = ""
        for i, v in enumerate(weights):
            weight_message += f"{i + 1}. {v}\n"
        bot.send_message(chat_id, weight_message)
    else:
        bot.send_message(chat_id, f"Нет данных о весах")


def create_date_keyboard(selected_date):
    keyboard = types.InlineKeyboardMarkup()
    prev_button = types.InlineKeyboardButton("Предыдущий день", callback_data='prev_day')
    next_button = types.InlineKeyboardButton("Следующий день", callback_data='next_day')
    choose_date_button = types.InlineKeyboardButton("Выбрать дату", callback_data='choose_date')
    keyboard.row(prev_button, next_button)
    keyboard.row(choose_date_button)

    return keyboard


def main():
    while True:
        try:
            with bot_lock:
                # Ваша основная логика бота...
                bot.polling(none_stop=True)

        except ApiTelegramException as e:
            if "Error code: 409" in str(e):
                # Обработка ошибки конфликта
                print("Ошибка конфликта, ожидание перед повторной попыткой...")
                time.sleep(5)  # Подождите несколько секунд перед повторной попыткой

            else:
                # Обработка других исключений API Telegram
                print(f"Ошибка Telegram API: {e}")

if __name__ == "__main__":
    main()
