import json
import random
from app.database.models import Character

class SceneSelector:

    def __init__(self, character_json, scenario_json) -> None:
        self.character_json = character_json
        self.scenario_json = scenario_json

    def select_random_character(self):
        with open(self.character_json, "r") as charater_file:
            characters = json.load(charater_file)

        return random.choice(characters)
    
    def select_random_setting(self):
        with open(self.scenario_json, "r") as settings_file:
            settings = json.load(settings_file)

        return random.choice(settings)
    
    def generate_random_scene(self):
        character = self.select_random_character()
        character = Character(*character)
        setting = self.select_random_setting()

        return Character(**character), setting

