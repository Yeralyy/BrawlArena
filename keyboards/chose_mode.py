from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def get_mode() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Solo🥇", callback_data="mode_solo"))
    builder.row(InlineKeyboardButton(text="Duo🤝", callback_data="mode_duo"))
    builder.adjust(2)
    return builder.as_markup()
    
    