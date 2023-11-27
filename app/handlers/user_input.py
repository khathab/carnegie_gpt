# handle user input

from aiogram import types, F
from aiogram.filters import CommandStart
from config import router
import logging
from database.db import register_user
from utils import download_media
from generation.generate_transcript import transcribe_audio
from generation.emotion_classifier import classify_face
from generation.decision import decision_engine
logger = logging.getLogger(__name__)


@router.message(F.voice)
async def handle_voice(message: types.Message):
    logger.info(f"Handling audiof from {message.chat.id}")
    # download audio for processing
    file_path = await download_media(message, message.voice)
    # transcribe audio
    text_transcript = transcribe_audio(file_path)
    await decision_engine(message.chat.id, text_transcript)

@router.message(F.photo)
async def handle_photo(message: types.Message):
    logger.info(f"Handling photo from {message.chat.id}")
    # download image for processing
    file_path = await download_media(message, message.photo[-1])
    # run through smile model
    smile_score = classify_face(file_path)
    # send message showing smile score
    await message.answer(text=f"Your smile score is: {smile_score}")

@router.message(CommandStart())
async def start_handle(message: types.Message):
    logger.info(f"Handling start from {message.chat.id}")
    # register user if they haven't been registered
    register_user(user_id=message.chat.id)

@router.message(F.text)
async def handle_text(message: types.Message):
    logger.info(f"Handling text from {message.chat.id}")
    await decision_engine(message.chat.id, message.text)


