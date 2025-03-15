import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

# Функция, которая будет вызываться при подписке нового пользователя
async def welcome_new_member(update: Update, context: CallbackContext):
    for user in update.message.new_chat_members:
        await update.message.reply_text(f"Спасибо что к нам присоединились, {user.first_name}!")

# Функция, которая будет вызываться при команде /neo
async def neo_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Вы выбрали команду /neo. Что-то интересное будет здесь!")

async def main():
    # Вставьте сюда ваш токен
    token = os.getenv("API_TOKEN")
     
    # Создаем Application и передаем ему токен вашего бота
    application = Application.builder().token(token).build()
    
    # Регистрируем обработчик для приветствия новых участников
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    
    # Регистрируем обработчик для команды /neo
    application.add_handler(CommandHandler("neo", neo_command))
    
    # Запускаем бота
    await application.run_polling()

# Запуск бота
if __name__ == "__main__":
    try:
        # Получаем текущий цикл событий
        loop = asyncio.get_event_loop()
        
        # Если цикл событий уже запущен, используем create_task
        if loop.is_running():
            loop.create_task(main())
        else:
            # Иначе запускаем цикл событий
            loop.run_until_complete(main())
    except Exception as e:
        print(f"Ошибка: {e}")