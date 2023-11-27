from config import bot
from ..database.db import get_principle

async def send_scenario():
    # get principle state

    # send scenario to user to practice a specific scenario
    pass

async def decision_engine(user_id: str, text: str):
    principle_state = get_principle(user_id)
    pass