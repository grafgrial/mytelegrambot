from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio
from aiohttp import web
import os

# Функция, которая будет вызываться при подписке нового пользователя
async def welcome_new_member(update: Update, context: CallbackContext):
    for user in update.message.new_chat_members:
        await update.message.reply_text(f"Спасибо что к нам присоединились, {user.first_name}!")

# Функция, которая будет вызываться при команде /neo
async def neo_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Вы выбрали команду /neo. Что-то интересное будет здесь!")

# Фиктивный HTTP-сервер
async def handle(request):
    return web.Response(text="Bot is running")

async def start_http_server():
    app = web.Application()
    app.router.add_get("/", handle)
    
    # Получаем порт из переменной окружения PORT (по умолчанию 10000)
    port = int(os.getenv("PORT", 8080))
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)  # Слушаем порт из переменной окружения
    await site.start()
    print(f"HTTP-сервер запущен на порту {port}")

async def main():
    # Вставьте сюда ваш токен
    token = os.getenv("API_TOKEN")
    
    # Создаем Application и передаем ему токен вашего бота
    application = Application.builder().token(token).build()
    
    # Регистрируем обработчик для приветствия новых участников
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    
    # Регистрируем обработчик для команды /neo
    application.add_handler(CommandHandler("neo", neo_command))
    
    # Запускаем фиктивный HTTP-сервер
    await start_http_server()
    
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