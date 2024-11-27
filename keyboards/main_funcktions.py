from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def options_keyboard() -> ReplyKeyboardMarkup:
    row = [
        [KeyboardButton(text="Available Touraments🏆")]
    ]
    return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True, input_field_placeholder="choose options")