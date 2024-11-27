from aiogram import Router, F

from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from filters.is_user_in_db import IsUserInDB
from filters.chat_filter import ChatTypeFIlter 

from aiogram.filters import CommandStart, Command


from keyboards.main_funcktions import options_keyboard
from keyboards.available_touraments import fetch_touraments


from database.BS import BS_DB

router = Router()

router.message.filter(
    ChatTypeFIlter("private")
)
router.message.filter(
    IsUserInDB()
)

@router.message(CommandStart())
async def welcom(
    message: Message
):
    await message.answer(text="<b>Привет👋\nВыберите из меню</b>⤵️", reply_markup=options_keyboard())

@router.message(F.text == "Available Touraments🏆")
async def fetch_awailable_touraments(message: Message, state: FSMContext):
    await message.answer(text="<b>Выберите Турнир👾</b>", reply_markup=fetch_touraments())

