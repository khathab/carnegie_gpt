from aiogram import types
from config import bot
from ..database.db import get_principle
from ..generation import generate_audio, generate_text

async def send_scenario(user_id, principle_state):
    # principle_state = get_principle(user_id)
    narrator_speech, character_speech = generate_text.generate_scenario(principle_state)
    character = generate_text.generate_character(principle_state)
    
    text = [narrator_speech, character_speech, "How do you respond"]
    character_names = ["Narrator",character,"Narrator"]
    file_path = generate_audio.generate_multiple_audio(text,character_names)

    voice = types.FSInputFile(file_path)
    await bot.send_voice(chat_id=user_id,voice=voice)

async def decision_engine(user_id: str, text: str):
    pass