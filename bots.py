from flask import Flask, request
from telegram import Update, Bot
from info import BOT_TOKEN

app = Flask(__name__)

# Замените на свой токен
bot = BOT_TOKEN # Вставьте сюда токен вашего бота

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="Привет от бота на Render!")
    return 'OK'

@app.route('/')
def index():
    return 'Bot is running!'

if __name__ == '__main__':
    app.run()