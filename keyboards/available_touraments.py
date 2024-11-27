from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def fetch_touraments() -> ReplyKeyboardMarkup:
    row = [
        [KeyboardButton(text="125 High School Tourament🏆")]
    ]
    return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True, input_field_placeholder="choose tourament")