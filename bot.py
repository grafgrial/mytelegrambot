import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from info import BOT_TOKEN
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

class Bot(Client):

    def __init__(self):
        super().__init__(
            bot_token=BOT_TOKEN,
            )
        
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome!\n\nTo get started, you can choose one of the following options:\n/menu - To view the menu\n/help - To learn how to use this bot\n/settings - To manage your account settings"
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Main menu:\n\n/buy - To buy access and start using our services\n/about - To learn more about our company\n/contact - To get in touch with us"
    )
    await update.message.reply_text(
        "Choose an option: ",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Buy", callback_data="buy"),
                    InlineKeyboardButton("About", callback_data="about"),
                ],
                [
                    InlineKeyboardButton("Contact", callback_data="contact"),
                ],
            ]
        )
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Thanks for choosing our services! \nTo get started, you can choose one of the following options:\n-Probationary period (7 days) \n-Pay for access and start using our services"
    )

    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Probationary period", callback_data="probationary"),
                InlineKeyboardButton("Pay for access", callback_data="pay"),
            ],
        ]
    )

    await update


app = Bot()
app.run()