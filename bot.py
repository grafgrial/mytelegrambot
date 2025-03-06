from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я ваш бот.')

def main() -> None:
    # Вставьте сюда ваш токен
    updater = Updater("ВАШ_ТОКЕН")

    dispatcher = updater.dispatcher

    # Регистрируем команду /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()