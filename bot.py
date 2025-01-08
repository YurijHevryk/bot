import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from yt_dlp import YoutubeDL

BOT_TOKEN = '7978463119:AAGKQlKvzoWPeZNLPq-Yw0SbV52S_WI42cc'
bot = telebot.TeleBot(BOT_TOKEN)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Збереження посилання для кожного користувача
user_data = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привіт! Надішліть мені посилання на відео з YouTube, і я допоможу тобі завантажити його.", reply_markup=None)

@bot.message_handler(func=lambda message: message.text and message.text.startswith("http"))
def download_videos(message):
    url = message.text.strip()
    chat_id = message.chat.id

    bot.send_message(chat_id, "Завантажую відео, зачекайте, будь ласка...")

    try:
        # Завантаження відео найвищої якості без звуку
        highest_quality_opts = {
            'format': 'bestvideo',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s_highest.%(ext)s'),
            'quiet': True,
        }

        with YoutubeDL(highest_quality_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'video')
            highest_video_path = os.path.join(DOWNLOAD_FOLDER, f"{video_title}_highest.{info['ext']}")

        # Надсилання відео найвищої якості без звуку
        with open(highest_video_path, 'rb') as video_file:
            bot.send_video(chat_id, video_file, caption="Відео найвищої якості без звуку")

        # Видалення відео після надсилання
        os.remove(highest_video_path)

        # Завантаження відео звичайної якості зі звуком
        normal_quality_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s_normal.%(ext)s'),
            'quiet': True,
        }

        with YoutubeDL(normal_quality_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            normal_video_path = os.path.join(DOWNLOAD_FOLDER, f"{video_title}_normal.{info['ext']}")

        # Надсилання відео звичайної якості зі звуком
        with open(normal_video_path, 'rb') as video_file:
            bot.send_video(chat_id, video_file, caption="Відео звичайної якості зі звуком")

        # Видалення відео після надсилання
        os.remove(normal_video_path)

    except Exception as e:
        bot.send_message(chat_id, f"Сталася помилка: {e}")

print("Бот працює...")
bot.polling()
