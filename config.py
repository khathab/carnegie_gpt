from aiogram import Bot, Dispatcher, Router
import openai
from elevenlabs import set_api_key
from dotenv import load_dotenv
import os
load_dotenv()

# load api keys
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

openai.api_key = OPENAI_API_KEY
set_api_key(ELEVENLABS_API_KEY)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()