import uuid
from elevenlabs import generate, DEFAULT_VOICE

# character voices
voice_ids = {
    "Myra": "4vlEMos5x2PbcYnHsT1l",
    "Alice": "CoZf1s84Vsecb9xR8WxN",
    "Bria": "F9h8mxs1RtuQ985zM6bB",
    "Tony": "L815I3iBG2ms7gWfsePu",
    "Kate": "NZpfeWklXUse3ELJ6xMG",
    "Jessica": "PUTbgKozbWQ3MXOcx0lh",
    "John": "Q9xFZkcFe0mkYObxXLOl",
    "Mark": "kDeIlneKsyEjD4gK3U0b",
    "Drew": "t9pa8vZ7tCoTLCLirl6c",
    "Narrator": "kGbsQLAWzUj4jK4NjsOh"
}

def generate_audio(text: str, voice_id: str):
    audio_bytes = generate(
        text=text,
        voice=voice_id
    )
    return audio_bytes

def generate_single_audio(text: str, character_name: str):
    voice_id = voice_ids[character_name]

    # if character not found, use default
    if voice_id is None:
        voice_id = DEFAULT_VOICE

    print("vOICE iD:", voice_id)
    audio_bytes = generate_audio(text, voice_id)
    file_path = f"audio_{uuid.uuid4()}.mp3"
    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_bytes)
    return file_path

def generate_multiple_audio(text: list, character_names: list):
    audio_data = []
    # adds each phrase to audio data
    for phrase, character_name in zip(text, character_names):
        voice_id = voice_ids[character_name]
        # if character not found, use default
        if voice_id is None:
            voice_id = DEFAULT_VOICE
        audio_bytes = generate_audio(phrase, voice_id)
        audio_data.append(audio_bytes)

    file_path = f"audio_{uuid.uuid4()}.mp3"

    # write audio data to mp3 file
    with open(file_path, "wb") as audio_file:
        for audio_bytes in audio_data:
            audio_file.write(audio_bytes)
    return file_path