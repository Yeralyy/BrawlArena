from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def fetch_parallel_keyboard() -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()

    for i in range(6, 12):
        builder.row(InlineKeyboardButton(text=str(i), callback_data=f"grade_{i}"))


    builder.adjust(3)

    return builder.as_markup()