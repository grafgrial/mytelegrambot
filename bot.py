import os
import logging
import asyncio
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Чтение токена из переменной окружения
API_TOKEN = os.getenv('API_TOKEN')  # Используем переменную окружения
if not API_TOKEN:
    raise ValueError("Не удалось загрузить API_TOKEN из переменных окружения.")

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

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

async def check_new_videos():
    """Периодически проверяет новые видео и отправляет их в Telegram."""
    global last_video_url
    while True:
        title, url, thumbnail = get_latest_video()
        if url and url != last_video_url:  # Если видео новое
            last_video_url = url  # Обновляем последнее отправленное видео
            # Отправляем новое видео всем пользователям
            for user_id in await get_all_users():
                try:
                    await bot.send_photo(user_id, thumbnail, caption=f"🎥 Новое видео!\n{title}\n🔗 {url}")
                except Exception as e:
                    logging.error(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
        await asyncio.sleep(300)  # Проверяем каждые 5 минут

async def get_all_users():
    """Возвращает список всех пользователей, которые начали диалог с ботом."""
    # В реальном проекте лучше использовать базу данных для хранения пользователей
    # Здесь для простоты возвращаем пустой список
    return []

if __name__ == '__main__':
    # Запуск бота в режиме long-polling
    loop = asyncio.get_event_loop()
    loop.create_task(check_new_videos())  # Запускаем фоновую задачу
    executor.start_polling(dp, skip_updates=True)