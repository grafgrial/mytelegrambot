import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# Функция, которая будет вызываться при подписке нового пользователя
def welcome_new_member(update: Update, context: CallbackContext):
    for user in update.message.new_chat_members:
        update.message.reply_text(f"Спасибо что к нам присоединились, {user.first_name}!")

# Функция, которая будет вызываться при команде /neo
def neo_command(update: Update, context: CallbackContext):
    update.message.reply_text("Вы выбрали команду /neo. Что-то интересное будет здесь!")
    
def main():
    # Вставьте сюда ваш токен
    #token = "YOUR_TELEGRAM_BOT_TOKEN"
    token = os.getenv("API_TOKEN")
    
 # Создаем Updater и передаем ему токен вашего бота
    updater = Updater(token, use_context=True)
    
    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher
    
    # Регистрируем обработчик для приветствия новых участников
    dp.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    
    # Регистрируем обработчик для команды /neo
    dp.add_handler(CommandHandler("neo", neo_command))
    
    # Запускаем бота
    updater.start_polling()
    
    # Работаем до тех пор, пока не будет нажата комбинация Ctrl+C
    updater.idle()

if __name__ == "__main__":
    main()