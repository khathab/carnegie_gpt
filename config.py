import os
from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv

load_dotenv()
# config telegram bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()