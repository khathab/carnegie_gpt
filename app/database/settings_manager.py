from mongodb import MongoDB
from models import Character

class SettingsManager(MongoDB):

    def __init__(self) -> None:
        super().__init__()
        self.users_collection = self.client['carnegie']["users"]

    def set_character(self, user_id: int, character: Character):
        self.users_collection.update_one(
            {"user_id":user_id},
            {
                "$set": {"current_character": character.model_dump()}
            }
        )

    def set_scenario(self, user_id: int, scenario: str):
        self.users_collection.update_one(
            {"user_id":user_id},
            {
                "$set": {"scenario": scenario}
            }
        )

    def set_setting(self, user_id: int, setting: str):
        self.users_collection.update_one(
            {"user_id":user_id},
            {
                "$set": {"setting": setting}
            }
        )

    def set_responding(self, user_id:int,responding:bool):
        self.users_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {"responding": responding}
            }
        )

    def is_responding(self, user_id: int):
        user_data = self.users_collection.find_one(
            {"user_id": user_id},
            {"responding": 1}
        )

        if user_data and "responding" in user_data and user_data["responding"]:
            return True
        return False

    def get_principle(self, user_id: int) -> int:
        """Retrieves the state of principle

        Args:
            user_id (int): unique telegram user id

        Returns:
            int: principle number
        """
        results = self.users_collection.find_one({"user_id":user_id})
        principle = results.get("principle",1)
        return principle

    def set_principle(self, user_id: int, principle_state: int):
        """
        Set the principle the user is currently on

        Args:
            user_id (int): unique telegram user id
            principle_state (int): state the user is currently on
        """
        self.users_collection.update_one(
            {"user_id":user_id},
            {
                "$set": {"principle_state":principle_state}
            }
        )

    def get_smile_score(self, user_id: int):
        results = self.users_collection.find_one({"user_id":user_id})
        smile_score = results.get("smile_score",0)
        return smile_score

    def set_smile_score(self, user_id: int, smile_score):
        self.users_collection.update_one(
            {"user_id":user_id},
            {
                "$set": {"smile_score": smile_score}
            }
        )

    def set_smile_record(self, user_id: int, smile_score_new: float) -> bool:
        """
        Sets the smile record if its higher than the current record

        Args:
            user_id (int): unique telegram user id
            smile_score_new (float): candidate new smile score

        Returns:
            bool: returns `True` if new smile score is higher than current smile score, `false` otherwise
        """
        smile_score_current = self.get_smile_score(user_id)

        if smile_score_new > smile_score_current:
            self.set_smile_score(user_id, smile_score_new)
            return True
        else:
            return False