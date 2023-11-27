from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from models import Message, User
from typing import List
import os

# connect to database
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)  # 5-second timeout for connection

try:
    client.admin.command('ismaster')
except ConnectionFailure:
    raise ValueError("Failed to connect to server {}".format(MONGODB_URI))

# create database
db = client['carnegie']
users_collection = db.users
# add user_id as unique index
users_collection.create_index("user_id", unique=True)

def add_user(user_id: int):
    """
    Add user to mongodb database

    Args:
        user_id (int): telegram unique id
    """
    new_user = User(user_id=user_id)
    try:
        users_collection.insert_one(new_user.model_dump())
    except Exception as e:
        print(f"Error inserting user: {e}")

def get_user(user_id: int) -> User:
    """
    Get user from mongodb database

    Args:
        user_id (int): unique telegram id

    Returns:
        User: _description_
    """
    result = users_collection.find_one(
        {"user_id": user_id}
    )
    try: 
        if result:
            return User(**result)
        return None
    except Exception as e:
        print(f"Failed to get user error: {e}")

def register_user(user_id: int):
    """
    Register user if they aren't registered already

    Args:
        user_id (int): unique telegram user id
    """
    user = get_user(user_id)
    if user is None:
        add_user(user_id)

def get_principle(user_id: int) -> int:
    """Retrieves the state of principle

    Args:
        user_id (int): unique telegram user id

    Returns:
        int: principle number
    """
    user = get_user(user_id)
    return user.principle_state

def set_principle(user_id: int, principle_state: int):
    """
    Set the principle the user is currently on

    Args:
        user_id (int): unique telegram user id
        principle_state (int): state the user is currently on
    """
    users_collection.update_one(
        {"user_id":user_id},
        {
            "$set": {"principle_state":principle_state}
        }
    )

def get_messages(user_id: int) -> List[Message]:
    """Retrieves user message history

    Args:
        user_id (int): unique telegram user id

    Returns:
        List[str]: user message history
    """
    user = get_user(user_id)
    return user.message_history

def add_message(user_id: int, text: str, sender: str):
    """
    Add message to user's message history

    Args:
        user_id (int): unique telegram user id
        text (str): message text
        sender (str): sender type, ie system, bot, user
    """
    message = Message(sender=sender,text=text)
    users_collection.update_one(
        {"user_id":user_id},
        {
            "$push": 
            {
                 "message_history": {"$each": [message.model_dump()], "$position": 0},
            }
        }
    )

def add_user_message(user_id: int, text: str):
    add_message(user_id=user_id,text=text,sender="user")

def add_system_message(user_id: int, text: str):
    add_message(user_id=user_id,text=text,sender="system")

def add_bot_message(user_id: int, text: str):
    add_message(user_id=user_id,text=text,sender="bot")