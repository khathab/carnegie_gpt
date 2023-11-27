from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from config import router, bot
from aiogram.filters.callback_data import CallbackData

class SelectPrinciple(CallbackData,prefix="principle"):
    principal_number: int

@router.message(Command("menu"))
async def send_menu(message: types.Message):
    # create keyboard options
    builder = InlineKeyboardBuilder()
    builder.button(text="1. Don’t criticize, condemn or complain",callback_data=SelectPrinciple(principal_number=1).pack())
    builder.button(text="2. Give honest and sincere appreciation",callback_data=SelectPrinciple(principal_number=2).pack())
    builder.button(text="3. Arouse in the other person an eager want",callback_data=SelectPrinciple(principal_number=3).pack())
    builder.button(text="4. Become genuinely interested in other people",callback_data=SelectPrinciple(principal_number=4).pack())
    builder.button(text="5. Smile",callback_data=SelectPrinciple(principal_number=5).pack())
    builder.button(text="6. Say people's names",callback_data=SelectPrinciple(principal_number=6).pack())
    builder.button(text="7. Be a good listener",callback_data=SelectPrinciple(principal_number=7).pack())
    builder.button(text="8. Talk in terms of the other person’s interests",callback_data=SelectPrinciple(principal_number=8).pack())
    # menu message
    text = "Pick a principle to practice!"
    # send menu
    await bot.send_message(chat_id=message.chat.id,text=text,reply_markup=builder.as_markup())

@router.callback_query(SelectPrinciple.filter())
async def process_principle_selection(callback_query: types.CallbackQuery):
    principle_callback = SelectPrinciple.unpack(callback_query.data)

    if principle_callback.principal_number == 1:
        
        # send scenario setup
    elif principle_callback.principal_number == 2:
    elif principle_callback.principal_number == 3:
    elif principle_callback.principal_number == 4:
    elif principle_callback.principal_number == 5:
    elif principle_callback.principal_number == 6:
    elif principle_callback.principal_number == 7:
    elif principle_callback.principal_number == 8:
    else:
        
        