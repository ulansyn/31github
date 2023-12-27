import re
from collections import Counter
import telebot
import srt
from io import BytesIO

BOT_TOKEN = 'MYTOKEN'
bot = telebot.TeleBot(BOT_TOKEN)


def get_word_counts(text):
    text = re.sub(r'[^\w\s]', '', text.lower())

    words = text.split()

    word_counts = Counter(words)

    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_word_counts


def send_word_counts(word_counts, chat_id):
    max_word_length = max(len(word) for word, count in word_counts)

    total_words = sum(count for word, count in word_counts)
    res = ""
    cnt = 1
    for i, (word, count) in enumerate(word_counts, start=1):
        percentage = (count / total_words) * 100
        escaped_word = word.replace('.', r'\.')
        for d in range(0, 10):
            if str(d) in escaped_word:
                break
        else:
            res += f"{str(cnt) + '.': <5} {escaped_word: <{max_word_length + 2}}{count: <15}{percentage:.4f}" + "\n"
            cnt += 1

    res = res.replace('.', r'.')
    print(res)
    while res:
        part, res = res[:4096], res[4096:]
        bot.send_message(chat_id, part)


@bot.message_handler(commands=['start'])
def handle_start(message):
    print(f'Function @handle_start was called for {message.chat.id}')


@bot.message_handler(content_types=['document'])
def handle_document(message):
    chat_id = message.chat.id

    if message.document.mime_type == 'application/x-subrip':
        file_info = bot.get_file(message.document.file_id)
        file_content = bot.download_file(file_info.file_path)

        srt_text = srt.compose(srt.parse(BytesIO(file_content).read().decode('utf-8')))

        word_counts = get_word_counts(srt_text)

        send_word_counts(word_counts, chat_id)
    else:
        bot.send_message(chat_id, "send an SRT file")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, "send an SRT file")


bot.polling(none_stop=True)
