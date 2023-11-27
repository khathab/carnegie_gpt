from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    sender: str
    text: str

class User(BaseModel):
    user_id: int
    message_history: List[Message] = []
    principle_state: int = 0
    smile_score: float = 0
