import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

''''BOT_TOKEN = environ.get('API_TOKEN', "")'''
BOT_TOKEN = os.getevn("API_TOKEN")