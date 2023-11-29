# handle user input

from aiogram import types, F
from aiogram.filters import CommandStart
from config import router
import logging
from ..database.db import register_user
from .utils import download_media
from ..generation.generate_transcript import transcribe_audio
from ..generation.emotion_classifier import classify_face
from ..generation.decision import decision_engine
from app.database import db
logger = logging.getLogger(__name__)


@router.message(F.voice)
async def handle_voice(message: types.Message):
    logger.info(f"Handling audio from {message.chat.id}")
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
    new_record = db.set_smile_record(message.chat.id, smile_score)
    smile_record = db.get_smile_score(message.chat.id)

    if new_record is True:
        # send message showing smile score
        await message.answer(text=f"Congrats new smile record: {smile_score:.2f}")
    else:
        await message.answer(text=f"Smile score: {smile_score:.2f}\nSmile score record: {smile_record:.2f}")


@router.message(CommandStart())
async def start_handle(message: types.Message):
    logger.info(f"Handling start from {message.chat.id}")
    # register user if they haven't been registered
    register_user(user_id=message.chat.id)

@router.message(F.text)
async def handle_text(message: types.Message):
    logger.info(f"Handling text from {message.chat.id}\nText: {message.text}")
    await decision_engine(message.chat.id, message.text)


