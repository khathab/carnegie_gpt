from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from config import router, bot
from aiogram.filters.callback_data import CallbackData
from ..generation.decision import send_scenario

principles = [
    "🚫 Avoid Criticism",
    "🤝 Show Appreciation",
    "💡 Inspire Desire",
    "🧑‍🤝‍🧑 Interest in Others",
    "😊 Smile",
    "📛 Use Names",
    "👂 Listen Well",
    "💬 Align Interests",
]

class SelectPrinciple(CallbackData, prefix="principle"):
    principle_state: int

@router.message(Command("menu"))
async def send_menu(message: types.Message):
    # create keyboard options
    builder = InlineKeyboardBuilder()
    for x, principle in enumerate(principles):
        builder.button(text=f"{x + 1}. {principle}", callback_data=SelectPrinciple(principle_state=x).pack())
    builder.adjust(1,1)
    # menu message
    text = "Pick a principle to practice!"
    # send menu
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=builder.as_markup())


@router.callback_query(SelectPrinciple.filter())
async def process_principle_selection(callback_query: types.CallbackQuery):
    principle_callback = SelectPrinciple.unpack(callback_query.data)
    user_id = callback_query.from_user.id
    principle = principle_callback.principle_state
    # set principle state in database
    # set_principle(user_id,principle)
    async with ChatActionSender.record_voice(chat_id=user_id,bot=bot,interval=3):
        await send_scenario(user_id,principle)