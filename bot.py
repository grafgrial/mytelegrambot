import os
import logging
from telegram import Update, LabeledPrice
from telegram.ext import Application, CommandHandler, MessageHandler, filters, PreCheckoutQueryHandler, CallbackContext

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Получите токен от BotFather

# Ссылки на курсы
COURSE_LINKS = {
    "course_beginner": "http://ruinfiniti.ru/kurs1",
    "course_advanced": "http://ruinfiniti.ru/kurs2",
}

# Цены на курсы (в копейках/центах)
PRICES = {
    "course_beginner": [LabeledPrice("Курс новичка в UE", 10000)],  # 100 рублей
    "course_advanced": [LabeledPrice("Курс продвинутой UE", 20000)],  # 200 рублей
}

# Команда /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Привет! Выберите курс для покупки:\n\n"
        "1. Курс новичка в UE - 100 рублей\n"
        "2. Курс продвинутой UE - 200 рублей\n\n"
        "Для покупки введите /buy_beginner или /buy_advanced."
    )

# Команда для покупки курса новичка
async def buy_beginner(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    title = "Курс новичка в UE"
    description = "Доступ к курсу для новичков в Unreal Engine."
    payload = "course_beginner"  # Уникальный идентификатор платежа
    provider_token = os.getenv("PAYMENT_PROVIDER_TOKEN")  # Токен платежного провайдера (от BotFather)
    currency = "RUB"
    prices = PRICES["course_beginner"]

    await context.bot.send_invoice(
        chat_id, title, description, payload, provider_token, currency, prices
    )

# Команда для покупки курса продвинутого
async def buy_advanced(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    title = "Курс продвинутой UE"
    description = "Доступ к курсу для продвинутых в Unreal Engine."
    payload = "course_advanced"  # Уникальный идентификатор платежа
    provider_token = os.getenv("PAYMENT_PROVIDER_TOKEN")  # Токен платежного провайдера (от BotFather)
    currency = "RUB"
    prices = PRICES["course_advanced"]

    await context.bot.send_invoice(
        chat_id, title, description, payload, provider_token, currency, prices
    )

# Обработка предварительного запроса оплаты
async def precheckout(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    await query.answer(ok=True)

# Обработка успешной оплаты
async def successful_payment(update: Update, context: CallbackContext):
    payment = update.message.successful_payment
    payload = payment.invoice_payload

    if payload == "course_beginner":
        link = COURSE_LINKS["course_beginner"]
    elif payload == "course_advanced":
        link = COURSE_LINKS["course_advanced"]
    else:
        link = None

    if link:
        await update.message.reply_text(f"Оплата прошла успешно! Ваша ссылка на курс: {link}")
    else:
        await update.message.reply_text("Оплата прошла успешно, но произошла ошибка. Свяжитесь с поддержкой.")
        logger.error(f"Ошибка при обработке платежа: неизвестный payload {payload}")

# Запуск бота
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("buy_beginner", buy_beginner))
    application.add_handler(CommandHandler("buy_advanced", buy_advanced))
    application.add_handler(PreCheckoutQueryHandler(precheckout))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()