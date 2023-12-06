from user_manager import UserManager
from settings_manager import SettingsManager
from chat_manager import ChatManager

class Database:

    def __init__(self) -> None:
        self.user_manager = UserManager()
        self.settings_manager = SettingsManager()
        self.chat_manager = ChatManager()

    ## Facade methods ##
    
    def add_user(self, user_id, user_name, full_name):
        self.user_manager.add_user(user_id, user_name, full_name)

    def get_user(self, user_id):
        return self.user_manager.get_user(user_id)

    def register_user(self, user_id, user_name, full_name):
        self.user_manager.register_user(user_id, user_name, full_name)

    def get_messages(self, user_id):
        return self.chat_manager.get_messages(user_id)

    def reset_messages(self, user_id):
        self.chat_manager.reset_messages(user_id)

    def add_user_message(self, user_id, text):
        self.chat_manager.add_user_message(user_id, text)

    def add_system_message(self, user_id, text):
        self.chat_manager.add_system_message(user_id, text)

    def add_bot_message(self, user_id, text):
        self.chat_manager.add_bot_message(user_id, text)

    def set_character(self, user_id, character):
        self.settings_manager.set_character(user_id, character)

    def set_scenario(self, user_id, scenario):
        self.settings_manager.set_scenario(user_id, scenario)

    def set_setting(self, user_id, setting):
        self.settings_manager.set_setting(user_id, setting)

    def set_responding(self, user_id, responding):
        self.settings_manager.set_responding(user_id, responding)

    def is_responding(self, user_id):
        return self.settings_manager.is_responding(user_id)

    def get_principle(self, user_id):
        return self.settings_manager.get_principle(user_id)

    def set_principle(self, user_id, principle_state):
        self.settings_manager.set_principle(user_id, principle_state)

    def get_smile_score(self, user_id):
        return self.settings_manager.get_smile_score(user_id)

    def set_smile_score(self, user_id, smile_score):
        self.settings_manager.set_smile_score(user_id, smile_score)

    def set_smile_record(self, user_id, smile_score_new):
        return self.settings_manager.set_smile_record(user_id, smile_score_new)
