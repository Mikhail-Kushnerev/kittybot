from dotenv import load_dotenv
from logging import error
import telegram
import requests
import os
import logging
from telegram.ext import CommandHandler, Updater, Filters, MessageHandler
from telegram.message import Message
from pprint import pprint

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)

URL = 'https://api.thecatapi.com/v1/images/search'


def start_work(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = telegram.ReplyKeyboardMarkup(
        [
            ['/newcat'],
            ['Выход']
        ], resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='спс, от души, брат-{}!'.format(name),
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_image())


def get_image():
    try:
        response = requests.get(URL)
    except Exception:
        logging.exception(f'Ошибка при запросе к основному API: {error}')
        NEW_URL = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(NEW_URL)
    rnd_cat = response.json()[0]['url']
    return rnd_cat


def put_image(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_image())


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='message')


def main():
    updater.dispatcher.add_handler(CommandHandler('start', start_work))
    updater.dispatcher.add_handler(CommandHandler('newcat', put_image))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
    updater.start_polling(poll_interval=3.0)
    updater.idle()


if __name__ == '__main__':
    main()


def send_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)


text = 'Вам телеграмма!'

send_message(text)
