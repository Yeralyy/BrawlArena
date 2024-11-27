from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def buy_ticket_solo() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="Pay💰", callback_data="buy_solo"))

    builder.adjust(1)
    return builder.as_markup()
    
def buy_ticket_duo() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="pay", callback_data="buy_duo"))

    builder.adjust(1)
    return builder.as_markup()
    
def verify() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="Оплатил👍", callback_data="bought"))

    builder.adjust(1)
    return builder.as_markup()

def payment(id, mode) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="✅", callback_data=f"yesv_{id}_{mode}"))
    builder.row(InlineKeyboardButton(text="❌", callback_data=f"notv_{id}_{mode}"))   

    builder.adjust(1)

    return builder.as_markup()