from pydantic import BaseModel
from typing import List, Optional

class Character(BaseModel):
    bio: str
    name: str
    age: str
    gender: str
    voice_id: str

class Message(BaseModel):
    sender: str
    text: str

class User(BaseModel):
    user_id: int
    user_name: str
    full_name: str
    message_history: List[Message] = []
    principle_state: int = 0
    scenario: Optional[str] = None
    setting: Optional[str] = None
    current_character: Optional[Character] = None
    smile_score: float = 0
    responding: bool = False