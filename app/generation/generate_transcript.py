from openai import OpenAI
client = OpenAI()

def transcribe_audio(file_path: str) -> str:
    audio_file = open(file_path, "rb")
    transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
    )
    return transcript