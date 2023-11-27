# handle user input

from aiogram import types, F
from aiogram.filters import CommandStart
from config import router
import logging
logger = logging.getLogger(__name__)


@router.message(F.voice)
async def handle_voice(message: types.Message):
    logger.info(f"Handling audiof from {message.chat.id}")
    # transcribe audio


@router.message(F.photo)
async def handle_photo(message: types.Message):
    logger.info(f"Handling photo from {message.chat.id}")
    # run photo through image processor

@router.message(CommandStart())
async def start_handle(message: types.Message):
    logger.info(f"Handling start from {message.chat.id}")
    # register user if they haven't been registered

@router.message(F.text)
async def handle_text(message: types.Message):
    logger.info(f"Handling text from {message.chat.id}")
    # run 


