from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from config import router, bot
from aiogram.filters.callback_data import CallbackData
from ..database.db import set_principle
from ..generation.decision import send_scenario

principles = [
"Don’t criticize, condemn or complain",
"Give honest and sincere appreciation",
"Arouse in the other person an eager want",
"Become genuinely interested in other people",
"Smile",
"Say their name",
"Be a good listener",
"Talk in terms of the other person’s interests",
]

class SelectPrinciple(CallbackData,prefix="principle"):
    principle_state: int

@router.message(Command("menu"))
async def send_menu(message: types.Message):
    # create keyboard options
    builder = InlineKeyboardBuilder()
    for x, principle in enumerate(principles):
        builder.button(text=f"{x + 1}. {principle}",callback_data=SelectPrinciple(principle_state=x+1).pack())
    builder.adjust(1,1)
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