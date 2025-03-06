import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Чтение токена из переменной окружения
TOKEN = os.getenv('API_TOKEN')
if not TOKEN:
    raise ValueError("Не удалось загрузить API_TOKEN из переменных окружения.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    await update.message.reply_text('Привет! Я ваш бот.')

async def main() -> None:
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Устанавливаем webhook
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    await application.bot.set_webhook(webhook_url)

    # Запускаем приложение
    await application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv('PORT', 8080)),
        webhook_url=webhook_url,
    )

if __name__ == '__main__':
    import asyncio

    # Проверяем, существует ли event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Запускаем main() без создания нового event loop
    if loop.is_running():
        # Если event loop уже запущен, используем create_task
        loop.create_task(main())
    else:
        # Если event loop не запущен, используем run_until_complete
        loop.run_until_complete(main())