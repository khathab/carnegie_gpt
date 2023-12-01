import json
import random
from app.database.models import Character

def generate_characters_settings():
    with open("./app/generation/character.json", "r") as charater_file:
        characters = json.load(charater_file)

    with open("./app/generation/location_settings.json", "r") as settings_file:
        settings = json.load(settings_file)

    random_character = random.choice(characters)
    random_setting = random.choice(settings)
    character = Character(**random_character)
    return character, random_setting

