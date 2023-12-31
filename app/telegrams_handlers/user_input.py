# handle user input

from aiogram import types, F
from aiogram.filters import CommandStart
from config import router
import logging
from app.database.database import Database
from app.generation.audio_generation import AudioGeneration
from app.generation.image_classifier import ImageClassifier
from .utils import download_media
from ..engine.decision import decision_engine
from app.database.database import Database
logger = logging.getLogger(__name__)

audio_gen = AudioGeneration()
image_classifier = ImageClassifier()
db = Database()

@router.message(F.voice)
async def handle_voice(message: types.Message):
    logger.info(f"Handling audio from {message.chat.id}")
    # download audio for processing
    file_path = await download_media(message, message.voice)
    # transcribe audio
    text_transcript = audio_gen.transcribe_audio(file_path)
    await decision_engine(message.chat.id, text_transcript)

@router.message(F.photo)
async def handle_photo(message: types.Message):
    logger.info(f"Handling photo from {message.chat.id}")
    # download image for processing
    file_path = await download_media(message, message.photo[-1])
    # run through smile model
    smile_score = image_classifier.classify_face(file_path)
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
    db.register_user(user_id=message.chat.id, user_name=message.chat.username, full_name=message.chat.full_name)

@router.message(F.text)
async def handle_text(message: types.Message):
    logger.info(f"Handling text from {message.chat.id}\nText: {message.text}")
    await decision_engine(message.chat.id, message.text)


