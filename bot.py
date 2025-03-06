import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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
    asyncio.run(main())