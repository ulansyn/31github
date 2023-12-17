import telebot
import json
import time
import zipfile
import os
from random import randint
from datetime import datetime
from telebot import types
from bottoken import bottoken
from json_complete import send_graphic
bot = telebot.TeleBot(bottoken)

all_commands = ['/start', '/addcategory', '/deletecategory', '/sendgraph', '/backup']

def markup():
    markup_val = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        button = types.KeyboardButton(category.capitalize())
        markup_val.add(button)
    return markup_val

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d.%m.%y")
        return True
    except ValueError:
        return False
    
def check_json(s):
    try:
        with open(f'{s}_data.json', 'r', encoding='utf-8') as file:
            x = json.load(file)
        for i in x:
            if not is_valid_date(i):
                return False
        return len(x) > 1
    except:
        return False

def is_command(s):
    return s in all_commands

def load_data(category):
    try:
        with open(f"{category}_data.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

def load_categories():
    try:
        with open("categories.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []

def load_active_category():
    try:
        with open("active_category.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

def save_active_category(active_category):
    with open("active_category.json", "w") as json_file:
        json.dump(active_category, json_file)

def save_categories(categories):
    with open("categories.json", "w") as json_file:
        json.dump(categories, json_file)

def current_category():
    active_category_name = [k for k, v in active_category.items() if v == 1]
    return active_category_name[0] if active_category_name else None

data = {category: load_data(category) for category in load_categories()}
active_category = load_active_category()
categories = load_categories()

@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, "Привет! Этот бот поможет тебе отслеживать твои данные. "
                                      "Сначала создай категорию по команде /addcategory, а затем выбери свою категорию и введи данные в виде '21.12.24 76.5'",
                     reply_markup=markup())


@bot.message_handler(commands=['backup'])
def send_all_json(message):
    today = datetime.now().strftime("%d.%m.%y")
    bot.send_message(message.chat.id, f"Бэкап данных на {today}")
    
    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)
    
    # Счетчик успешно добавленных категорий
    successful_backup_count = 0

    for i in load_categories():
        json_file_path = f'{i}_data.json'
        temp_json_path = os.path.join(temp_dir, f'{i}_data.json')
        
        try:
            with open(json_file_path, 'r') as src_json, open(temp_json_path, 'w') as dest_json:
                dest_json.write(src_json.read())

            successful_backup_count += 1
        except FileNotFoundError:
            bot.send_message(message.chat.id, f"Ошибка: Файл {json_file_path} не найден.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка при копировании файла {json_file_path}: {e}")

    if successful_backup_count > 0:
        zip_filename = f'backup_{today}.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            for i in load_categories():
                temp_json_path = os.path.join(temp_dir, f'{i}_data.json')
                zip_file.write(temp_json_path, f'{i}_data.json')

        chat_id = message.chat.id
        with open(zip_filename, 'rb') as zip_file:
            bot.send_document(chat_id, zip_file)

        os.remove(zip_filename)

        bot.send_message(message.chat.id, f"Успешно сохранено категорий: {successful_backup_count}")

    for i in load_categories():
        temp_json_path = os.path.join(temp_dir, f'{i}_data.json')
        os.remove(temp_json_path)
    os.rmdir(temp_dir)
    
    if successful_backup_count == 0:
        bot.send_message(message.chat.id, f"Нет категорий для сохранения")


@bot.message_handler(commands=['sendgraph'])
def send_graph(message):
    bot.send_message(message.chat.id, "Выберите категорию для отправки графика:", reply_markup=markup())
    bot.register_next_step_handler(message, send_selected_graph)

def send_selected_graph(message):
    category = message.text.lower()
    if is_command(category):
        bot.send_message(message.chat.id, "Недопустимая категория!")
        bot.send_message(message.chat.id, "Чтобы получить график нужной категории, введите /sendgraph, а затем выберите категорию")
    else:    
        if check_json(category):
            send_graphic(category)
            with open('title.png', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.send_message(message.chat.id, "Недостаточно данных!")

@bot.message_handler(commands=['addcategory'])
def add_category(message):
    bot.send_message(message.chat.id, "Введите название новой категории:")
    bot.register_next_step_handler(message, process_new_category)

def process_new_category(message):
    new_category = message.text.lower()
    if new_category in data:
        bot.send_message(message.chat.id, "Такая категория уже существует! Чтобы добавить категорию, введите команду /addcategory")
    elif is_command(new_category):
        bot.send_message(message.chat.id, "Недопустимая категория! Введите другое название категории, после ввода команды /addcategory")
    else:
        categories.append(new_category)
        data[new_category] = {}
        active_category[new_category] = 0  # кстанавливаем новую категорию неактивной
        save_categories(categories)
        save_active_category(active_category)  # cохраняем изменения
        with open(f"{new_category}_data.json", "w") as json_file:
                json.dump(data[new_category], json_file)

        bot.send_message(message.chat.id, f"Новая категория '{new_category.capitalize()}' добавлена.",
                         reply_markup=markup())

@bot.message_handler(commands=['deletecategory'])
def delete_category(message):

    bot.send_message(message.chat.id, "Выберите категорию для удаления:", reply_markup=markup())
    bot.register_next_step_handler(message, process_delete_category)

def process_delete_category(message):
    category_to_delete = message.text.lower()

    if category_to_delete in categories:
        categories.remove(category_to_delete)
        data.pop(category_to_delete, None)
        active_category.pop(category_to_delete, None)
        save_categories(categories)
        save_active_category(active_category)
        os.rename(f'{category_to_delete}_data.json', f'удалено_{randint(1,10000)}{category_to_delete}_data.json')
        bot.send_message(message.chat.id, f"Категория '{category_to_delete.capitalize()}' удалена.",
                         reply_markup=markup())
        bot.send_message(message.chat.id, "Чтобы удалить категорию, введите команду /deletecategory", reply_markup=markup())
    else:
        bot.send_message(message.chat.id, "Недопустимая категория. Выберите существующую категорию.", reply_markup=markup())
        bot.send_message(message.chat.id, "Чтобы удалить категорию, еще раз введите команду /deletecategory")

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
        elif category is None:
            bot.send_message(message.chat.id, "Выберите категорию с помощью кнопок.")
        else:
            bot.send_message(message.chat.id, "Недопустимая категория. Выберите существующую категорию.")
    else:
        bot.send_message(message.chat.id, "Некорректный формат. Пожалуйста, введите данные в формате 'дата значение'.")

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, timeout=5)
        except:
            print("Переподключение через 10 сек")
            time.sleep(10)
