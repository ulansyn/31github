import telebot
import json
from datetime import datetime
from telebot import types

bot = telebot.TeleBot('MYTOKEN')


def load_data(category):
    try:
        with open(f"{category}_data.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

def load_active_category():
    try:
        with open("active_category.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {"отжимания": 0, "подтягивания": 0, "вес": 0}

# Сохранение текущей активной категории
def save_active_category(active_category):
    with open("active_category.json", "w") as json_file:
        json.dump(active_category, json_file)
# текущая категория    
def current_category():
    active_category_name = [k for k, v in active_category.items() if v == 1]
    return active_category_name[0] if active_category_name else None

data = {'отжимания': load_data('отжимания'), 'подтягивания': load_data('подтягивания'), 'вес': load_data('вес')}
active_category = load_active_category()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    categories = ["отжимания", "подтягивания", "вес"]

    for category in categories:
        button = types.KeyboardButton(category.capitalize())
        markup.add(button)

    bot.send_message(message.chat.id, "Привет! Этот бот поможет тебе отслеживать твои тренировки. "
                                      "Выбери категорию и введи значение через пробел, например, 'вес 21.12.23 77.5'.",
                     reply_markup=markup)
    
# данные в джсон
@bot.message_handler(commands=['getjson'])
def get_json(message):
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    bot.send_message(message.chat.id, f"Текущие данные:\n{json_str}")

@bot.message_handler(func=lambda message: message.text.lower() in data)
def handle_category(message):
    global active_category
    category = message.text.lower()
    active_category = {k: 1 if k == category else 0 for k in active_category}
    save_active_category(active_category)
    bot.send_message(message.chat.id, f"Выбрана категория '{category.capitalize()}' для ввода данных.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.split()

    if len(text) == 2:
        category = current_category()
        date = text[0]
        value = float(text[1])

        if category in data:
            if date in data[category]:
                data[category][date].append(value)
            else:
                data[category][date] = [value]

            with open(f"{category}_data.json", "w") as json_file:
                json.dump(data[category], json_file)

            bot.send_message(message.chat.id, f"Данные добавлены для категории '{category}' на {date}: {value}")
        else:
            bot.send_message(message.chat.id, "Недопустимая категория. Выберите отжимания, подтягивания или вес.")
    else:
        bot.send_message(message.chat.id, "Некорректный формат. Пожалуйста, введите данные в формате 'категория дата значение'.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
