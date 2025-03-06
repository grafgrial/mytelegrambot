import os
import logging
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.webhook import WebhookRequestHandler
from aiogram.utils.executor import start_webhook
from aiohttp import web

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Чтение токена из переменной окружения
API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    raise ValueError("Не удалось загрузить API_TOKEN из переменных окружения.")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# URL канала YouTube
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/@GrAlUnrealEngine/videos"

# Переменная для хранения последнего отправленного видео
last_video_url = None

def get_latest_video():
    """Получает последнее видео с канала YouTube."""
    try:
        # Загружаем страницу
        response = requests.get(YOUTUBE_CHANNEL_URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем последнее видео
        video = soup.find("a", {"class": "yt-simple-endpoint style-scope ytd-grid-video-renderer"})
        if video:
            video_title = video.get("title")
            video_url = "https://www.youtube.com" + video.get("href")
            thumbnail_url = f"https://img.youtube.com/vi/{video_url.split('v=')[1]}/maxresdefault.jpg"
            return video_title, video_url, thumbnail_url
        else:
            return None, None, None
    except Exception as e:
        logging.error(f"Ошибка при получении видео: {e}")
        return None, None, None

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Обработчик команды /start."""
    await message.reply("Привет! Я бот, который отслеживает последние видео с канала GrAlUnrealEngine.")

@dp.message_handler(commands=['latest_video'])
async def send_latest_video(message: types.Message):
    """Отправляет последнее видео."""
    title, url, thumbnail = get_latest_video()
    if title and url and thumbnail:
        # Отправляем сообщение с превью
        await message.reply_photo(thumbnail, caption=f"🎥 {title}\n🔗 {url}")
    else:
        await message.reply("Не удалось получить последнее видео.")

async def on_startup(app):
    """Действия при запуске сервера."""
    # Установка webhook
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    await bot.set_webhook(webhook_url)
    logging.info(f"Webhook установлен на {webhook_url}")

async def on_shutdown(app):
    """Действия при завершении работы сервера."""
    # Удаление webhook
    await bot.delete_webhook()
    logging.info("Webhook удален")

# Создание aiohttp приложения
app = web.Application()

# Регистрация обработчика webhook
webhook_request_handler = WebhookRequestHandler(dp)  # Передаем только диспетчер
app.router.add_post('/webhook', webhook_request_handler)

# Запуск сервера
if __name__ == '__main__':
    # Укажите порт, который будет прослушивать сервер
    PORT = int(os.getenv('PORT', 8080))

    # Запуск вебхука
    start_webhook(
        dispatcher=dp,
        webhook_path='/webhook',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port=PORT,
    )