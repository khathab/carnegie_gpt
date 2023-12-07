from elevenlabs import generate, voices, set_api_key
from openai import OpenAI
import openai
import json
from dotenv import load_dotenv
import os

class AudioGeneration:

    def __init__(self) -> None:
        load_dotenv()
        ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        set_api_key(ELEVENLABS_API_KEY)
        openai.api_key = OPENAI_API_KEY
        self.client = OpenAI()

    def generate_audio(self, text: str, voice_id: str) -> bytes:
        audio_bytes = generate(
            text=text,
            voice=voice_id,
            model="eleven_turbo_v2"
        )
        return audio_bytes

    def generate_single_audio(self, text: str, voice_id) -> bytes:
        audio_bytes = self.generate_audio(text, voice_id)
        return audio_bytes

    def transcribe_audio(self, file_path: str) -> str:
        audio_file = open(file_path, "rb")
        transcript = self.client.audio.transcriptions.create(
        model="whisper-2", 
        file=audio_file, 
        response_format="text"
        )
        return transcript
    
    @staticmethod
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

