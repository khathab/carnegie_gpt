from mongodb import MongoDB
from models import Message
from typing import List

class ChatManager(MongoDB):

    def __init__(self) -> None:
        super().__init__()
        self.users_collection = self.client['carnegie']["users"]

    def get_messages(self, user_id: int) -> List[str]:
        """Retrieves user message history

        Args:
            user_id (int): unique telegram user id

        Returns:
            List[str]: user message history
        """
        results = self.users_collection.find_one(
            {"user_id":user_id}
            )
        message_history = results.get("message_history",[])
        return message_history

    def reset_messages(self, user_id: int):
        """
        Reset user message history

        Args:
            user_id (int): unique telegram user id

        """
        self.users_collection.update_one(
            {"user_id":user_id},
            {
                "$set": {"message_history":[]}
            }
        )

    def add_message(self, user_id: int, text: str, sender: str):
        """
        Add message to user's message history

        Args:
            user_id (int): unique telegram user id
            text (str): message text
            sender (str): sender type, ie system, bot, user
        """
        message = Message(sender=sender,text=text)
        self.users_collection.update_one(
            {"user_id":user_id},
            {
                "$push": 
                {
                    "message_history": {"$each": [message.model_dump()], "$position": 0},
                }
            }
        )

    def add_user_message(self, user_id: int, text: str):
        self.add_message(user_id=user_id,text=text,sender="user")

    def add_system_message(self, user_id: int, text: str):
        self.add_message(user_id=user_id,text=text,sender="system")

    def add_bot_message(self, user_id: int, text: str):
        self.add_message(user_id=user_id,text=text,sender="bot")