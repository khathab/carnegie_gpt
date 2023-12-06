from mongodb import MongoDB
from models import User

class UserManager(MongoDB):

    def __init__(self) -> None:
        super().__init__()
        self.users_collection = self.client['carnegie']["users"]
        self.users_collection.create_index("user_id", unique=True)

    def add_user(self, user_id: int, user_name: str, full_name: str):
        """
        Add user to mongodb database

        Args:
            user_id (int): telegram unique id
        """
        new_user = User(user_id=user_id,user_name=user_name,full_name=full_name)
        try:
            self.users_collection.insert_one(new_user.model_dump())
        except Exception as e:
            print(f"Error inserting user: {e}")

    def get_user(self, user_id: int) -> User:
        """
        Get user from mongodb database

        Args:
            user_id (int): unique telegram id

        Returns:
            User: _description_
        """
        result = self.users_collection.find_one(
            {"user_id": user_id}
        )
        try: 
            if result:
                return User(**result)
            return None
        except Exception as e:
            print(f"Failed to get user error: {e}")

    def register_user(self, user_id: int, user_name: str, full_name: str):
        """
        Register user if they aren't registered already

        Args:
            user_id (int): unique telegram user id
        """
        user = self.get_user(user_id)
        if user is None:
            self.add_user(user_id, user_name, full_name)