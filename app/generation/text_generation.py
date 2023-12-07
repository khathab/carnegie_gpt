import yaml
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from app.database.database import Database
from app.generation.scene_generation import SceneSelector

class StoryGenerator:
    def __init__(self, prompts_file, principles_file, model_name="gpt-3.5-turbo", max_tokens=100):
        self.db = Database()
        self.scene_selector = SceneSelector()
        self.model = ChatOpenAI(model=model_name, max_tokens=max_tokens, model_kwargs={"stop": ["\n"]})
        self.prompts = self.load_yaml(prompts_file)
        self.principles = self.load_json(principles_file)
        self.chains = self.create_chains()

    @staticmethod
    def load_yaml(file_path):
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def load_json(file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    def create_chains(self):
        chains = {}
        for prompt_type in ['scenario', 'narration', 'speech', 'response']:
            prompt_template = ChatPromptTemplate.from_template(self.prompts[f"{prompt_type}_prompt"])
            chains[prompt_type] = prompt_template | self.model | StrOutputParser()
        return chains

    def generate_scenario(self, principle_state, user_id):
        character, setting = self.scene_selector.generate_random_scene()
        user = self.db.get_user(user_id)
        principle_text = self.principles[principle_state]

        scenario_data = {
            "principle": principle_text,
            "character_name": character.name,
            "user_name": user.full_name,
            "bio": character.bio,
            "age": character.age,
            "gender": character.gender,
            "setting": setting
        }

        scenario = self.chains['scenario'].invoke(scenario_data)
        narrator_speech = self.chains['narration'].invoke({"scenario": scenario})
        character_speech = self.chains['speech'].invoke({**scenario_data, "scenario": scenario})

        self.update_database(user_id, principle_state, character, scenario, setting, character_speech)
        return narrator_speech, character_speech
    
    def generate_response(self, user_id, user_message):
        user = self.db.get_user(user_id)
        principle_text = self.principles[user.principle_state]
        self.db.add_user_message(user_id, f"{user.full_name}: {user_message}")

        message_history = self.get_message_history(user_id)

        response_data = {
            "principle": principle_text,
            "character_name": user.current_character.name,
            "user_name": user.full_name,
            "bio": user.current_character.bio,
            "age": user.current_character.age,
            "gender": user.current_character.gender,
            "setting": user.setting,
            "scenario": user.scenario,
            "history": message_history
        }

        character_speech = self.chains['response'].invoke(response_data)
        self.db.add_bot_message(user_id, f"{user.current_character.name}: {character_speech}")

        return character_speech

    def get_message_history(self, user_id, latest_n=10):
        message_list = self.db.get_messages(user_id)
        return "\n".join(message_list[-latest_n:][::-1])

    def update_database(self, user_id, principle_state, character, scenario, setting, character_speech):
        self.db.reset_messages(user_id)
        self.db.set_principle(user_id, principle_state=principle_state)
        self.db.set_character(user_id, character)
        self.db.set_scenario(user_id, scenario)
        self.db.set_setting(user_id, setting)
        formatted_message = f"{character.name}: {character_speech}"
        self.db.add_bot_message(user_id, formatted_message)
