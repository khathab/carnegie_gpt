from aiogram import types
from config import bot
from ..database import db
from ..generation import generate_audio, generate_text

async def send_scenario(user_id, principle_state):
    # principle_state = get_principle(user_id)
    if is_locked_double_texting(user_id):
        return
    narrator_speech, character_speech = generate_text.generate_scenario(principle_state,user_id)
    user = db.get_user(user_id)

    narration_path = generate_audio.generate_single_audio(narrator_speech,"kGbsQLAWzUj4jK4NjsOh")
    speech_path = generate_audio.generate_single_audio(character_speech,user.current_character.voice_id)
    narration_audio = types.FSInputFile(narration_path)
    speech_audio = types.FSInputFile(speech_path)

    #await bot.send_message(chat_id=user_id,text=narrator_speech)
    await bot.send_voice(chat_id=user_id,voice=narration_audio)
    #await bot.send_message(chat_id=user_id,text=character_speech)
    await bot.send_voice(chat_id=user_id,voice=speech_audio)
    db.set_responding(user_id, False)

async def decision_engine(user_id: str, text: str):
    if is_locked_double_texting(user_id):
        return
    user = db.get_user(user_id)
    character_speech = generate_text.generate_response(user_id,text)
    speech_path = generate_audio.generate_single_audio(character_speech,user.current_character.voice_id)
    speech_audio = types.FSInputFile(speech_path)
    #await bot.send_message(chat_id=user_id,text=character_speech)
    await bot.send_voice(chat_id=user_id,voice=speech_audio)
    db.set_responding(user_id, False)

def is_locked_double_texting(user_id):
    """
    Used for toggling user, so only one messages is sent for each group of messages within a time period
    """
    if db.is_responding(user_id):
        return True
    db.set_responding(user_id,True)
    return False