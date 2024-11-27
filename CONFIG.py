from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


""" BOT TOKEN """
TOKEN = "7651191457:AAGhNKVyQw-PP8C1dZy49dMwlL4PfeGGmhY"

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)