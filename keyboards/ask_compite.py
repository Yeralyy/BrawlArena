from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def get_compit() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Принять✅", callback_data="accept"))
    builder.adjust(1)
    return builder.as_markup()
    
    