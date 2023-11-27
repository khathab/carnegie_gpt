from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from config import router, bot
from aiogram.filters.callback_data import CallbackData
from ..database.db import set_principle
from ..generation.decision import send_scenario

principles = [
"Principle 1: Don’t criticize, condemn or complain",
"Principle 2: Give honest and sincere appreciation",
"Principle 3: Arouse in the other person an eager want",
"Principle 4: Become genuinely interested in other people",
"Principle 5: Smile",
"Principle 6: Remember that a person’s name is to that person the sweetest and most important sound in any language",
"Principle 7: Be a good listener",
"Principle 8: Talk in terms of the other person’s interests",
]

class SelectPrinciple(CallbackData,prefix="principle"):
    principle_state: int

@router.message(Command("menu"))
async def send_menu(message: types.Message):
    # create keyboard options
    builder = InlineKeyboardBuilder()
    for x, principle in enumerate(principles):
        builder.button(text=f"{x + 1}. {principle}",callback_data=SelectPrinciple(principle_state=x+1).pack())
    # menu message
    text = "Pick a principle to practice!"
    # send menu
    await bot.send_message(chat_id=message.chat.id,text=text,reply_markup=builder.as_markup())

@router.callback_query(SelectPrinciple.filter())
async def process_principle_selection(callback_query: types.CallbackQuery):
    principle_callback = SelectPrinciple.unpack(callback_query.data)
    principle = principle_callback.principle_state
    # set principle state in database
    set_principle(principle)
    await bot.send_message(f"You have chosen Principle: {principle}. {principles[principle-1]}.\nLets practice!")
    await send_scenario()