from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! \nTo get started, you can choose one of the following options: \n/help - To learn how to use this bot \n/buy - To buy access and start using our services \n/settings - To manage your account settings"
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Thanks for choosing our services! \nTo get started, you can choose one of the following options: \n-Probationary period (7 days) \n-Pay for access and start using our services"
    )

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("Probationary period")
    item2 = KeyboardButton("Pay for access")
    markup.add(item1, item2)

    await update.message.reply_text("Please select an option:", reply_markup=markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "This bot provides the following commands: \n/start - To start\n/buy - To buy access and start using our services\n/settings - To manage your account settings"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Probationary period":
        await update.message.reply_text("You chose the probationary period.")
    elif text == "Pay for access":
        await update.message.reply_text("You chose to pay for access.")

if __name__ == '__main__':
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    start_handler = CommandHandler('start', start)
    buy_handler = CommandHandler('buy', buy)
    help_handler = CommandHandler('help', help_command)
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)

    application.add_handler(start_handler)
    application.add_handler(buy_handler)
    application.add_handler(help_handler)
    application.add_handler(message_handler)

    application.run_polling()