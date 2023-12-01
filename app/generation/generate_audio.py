import uuid
from elevenlabs import generate, voices
import json

def generate_audio(text: str, voice_id: str):
    audio_bytes = generate(
        text=text,
        voice=voice_id,
        model="eleven_turbo_v2"
    )
    return audio_bytes

def generate_single_audio(text: str, voice_id):

    audio_bytes = generate_audio(text, voice_id)
    file_path = f"audio_{uuid.uuid4()}.mp3"
    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_bytes)
    return file_path

def generate_multiple_audio(text: list, voice_ids: list):
    audio_data = []
    # adds each phrase to audio data
    for phrase, voice_id in zip(text, voice_ids):
        audio_bytes = generate_audio(phrase, voice_id)
        audio_data.append(audio_bytes)

    file_path = f"audio_{uuid.uuid4()}.mp3"

    # write audio data to mp3 file
    with open(file_path, "wb") as audio_file:
        for audio_bytes in audio_data:
            audio_file.write(audio_bytes)
    return file_path

def create_character_json():
    voices_list = voices()
    characters = []
    for voice in voices_list:
        character = {
            "name": voice.name,
            "voice_id": voice.voice_id,
            "gender": voice.labels["gender"],
            "age": voice.labels["age"]
        }
        characters.append(character)

    with open("./app/generation/character.json","w") as file:
        json.dump(characters, file,indent=4)
