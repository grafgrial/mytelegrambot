import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(bot, update):
    bot.send_message(chat_id=update.effective_chat.id, text="Welcome! \nTo get started, you can choose one of the following options: \n/help - To learn how to use this bot \n/buy - To buy access and start using our services \n/settings - To manage your account settings")

def buy(bot, update):
    bot.send_message(chat_id=update.effective_chat.id, text="Thanks for choosing our services! \nTo get started, you can choose one of the following options: \n-Probationary period (7 days) \n-Pay for access and start using our services")

    markup = telegram.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telegram.KeyboardButton("Probationary period")
    item2 = telegram.KeyboardButton("Pay for access")
    markup.add(item1, item2)

    bot.send_message(chat_id=update.effective_chat.id, text="Please select an option:", reply_markup=markup)

def help(bot, update):
    bot.send_message(chat_id=update.effective_chat.id, text="This bot provides the following commands: \n/start - To start\n/buy - To buy access and start using our services\n/settings - To manage your account settings")