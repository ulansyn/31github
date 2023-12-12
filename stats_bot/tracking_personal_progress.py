import telebot
import json
from datetime import datetime
from telebot import types

bot = telebot.TeleBot('TOKEN')
def load_active_category():
    try:
        with open("active_category.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {"категория1": 0, "категория2": 0, "категория3": 0}

data = {'категория1': {}, 'категория2': {}, 'категория3': {}}
active_category = load_active_category()

def load_data(category):
    try:
        with open(f"{category}_data.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

def save_active_category(active_category):
    with open("active_category.json", "w") as json_file:
        json.dump(active_category, json_file)

def current_category():
    active_category_name = [k for k, v in active_category.items() if v == 1]
    return active_category_name[0] if active_category_name else None

def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    categories = ["категория1", "категория2", "категория3"]

    for category in categories:
        button = types.KeyboardButton(category.capitalize())
        markup.add(button)

    bot.send_message(message.chat.id, "Привет! Этот бот поможет тебе отслеживать твои тренировки. "
                                      "Выбери категорию и введи значение через пробел, например, 'вес 21.12.23 77.5'.",
                     reply_markup=markup)

def get_json_handler(message):
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    bot.send_message(message.chat.id, f"Текущие данные:\n{json_str}")

def handle_category_selection(message, active_category):
    category = message.text.lower()
    active_category = {k: 1 if k == category else 0 for k in active_category}
    save_active_category(active_category)
    bot.send_message(message.chat.id, f"Выбрана категория '{category.capitalize()}' для ввода данных.")

def handle_text_input(message, data):
    text = message.text.split()
    print(current_category())
    if len(text) == 2:
        category = current_category()
        date = text[0]
        try:
            value = float(text[1].replace(',', '.'))
        except ValueError:
            bot.send_message(message.chat.id, 'Введите корректные данные!')
            return

        if category in data:
            update_data(category, date, value)
            bot.send_message(message.chat.id, f"Данные добавлены для категории '{category}' на {date}: {value}")
        else:
            bot.send_message(message.chat.id, "Недопустимая категория. Выберите категория1, категория2 или категория3.")
    else:
        bot.send_message(message.chat.id, "Некорректный формат. Пожалуйста, введите данные в формате 'дата значение'")

def update_data(category, date, value):
    if date in data[category]:
        data[category][date].append(value)
    else:
        data[category][date] = [value]

    with open(f"{category}_data.json", "w") as json_file:
        json.dump(data[category], json_file)


@bot.message_handler(commands=['start'])
def start_message(message):
    start_handler(message)


@bot.message_handler(commands=['getjson'])
def get_json_message(message):
    get_json_handler(message)


@bot.message_handler(func=lambda message: message.text.lower() in data)
def category_selection_message(message):
    global active_category
    handle_category_selection(message, active_category)


@bot.message_handler(func=lambda message: True)
def text_input_message(message):
    handle_text_input(message, data)


if __name__ == "__main__":
    bot.polling(none_stop=True)
