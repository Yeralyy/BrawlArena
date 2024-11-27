from aiogram import Router, F

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from filters.chat_filter import ChatTypeFIlter
from aiogram.filters import Command, CommandStart
from forums.login_forum import LoginForum
from constants import WELCOM_TEXT

from database.BS import BS_DB

from filters.invete_filter import BrawlStarsLinkFilter

from keyboards.login_parallel import fetch_parallel_keyboard

from keyboards.reg_aprove import get_aprovee
from keyboards.main_funcktions import options_keyboard

from constants import WARNING_TEXT, ASK_PHONE, ASK_NOT_BLOCK, ASK_PARALLEL, ASK_NAME, ASK_FRIEND_REQUEST

import re
router = Router()


# /start cmd, to login user
@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAMYZ0BdWWSMHcrSj5iQLF8uwxG7ZTQAAnQOAAIexlBL4iV2PyjU3i82BA")
    await message.answer(text=WELCOM_TEXT)
    await message.answer(WARNING_TEXT)
    await message.answer(ASK_NAME)
    
    await state.set_state(LoginForum.full_name)

@router.message(Command("instruction"))
async def instruction(message: Message):
    await message.answer_video(video="BAACAgIAAxkBAAMxZ0XPa2js-AyIKwhbYnyOPscxYsAAAgJbAAIb_zBK1fL-QTYAARKcNgQ", caption="📹Видеоинструкция")

# pattern for name
pattern = r'^[А-Яа-яӘәӨөҮүҚқҒғҢңШшЧчЫыІіЕеЮюЯя]+ [А-Яа-яӘәӨөҮүҚқҒғҢңШшЧчЫыІіЕеЮюЯя]+$'


# in case pattern match:
@router.message(LoginForum.full_name, F.text.regexp(re.compile(pattern)))
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    
    await message.reply(text="<b>Отлично👍✅</b>")
    await message.answer(text=ASK_PHONE)

    await state.set_state(LoginForum.phone_number)

# in case pattern unmatch
@router.message(LoginForum.full_name)
async def wrong_name_format(message: Message):
    await message.answer("<b>Убедитесь что вы правильно ввели имя, как на примере\n\nИспользуйте только кирилицу!</b>")

# hndler for phone number
@router.message(LoginForum.phone_number, F.text.regexp(re.compile(r'^\+7 \d{3} \d{3} \d{2} \d{2}$')))
async def get_number(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    await message.reply(text="<b>Номер телефона сохранен👍✅</b>")

    await message.answer(text=ASK_PARALLEL, reply_markup=fetch_parallel_keyboard())

    await state.set_state(LoginForum.parallel)
    
# in case wrong phone number pattern:
@router.message(LoginForum.phone_number)
async def wrong_phone_number(message: Message):
    await message.answer("<b>Неверный формат номера</b>\n\n<i>Используйте формат выше</i>")

# handle parallel chose parallel callback
@router.callback_query(F.data.startswith('grade_'), LoginForum.parallel)
async def get_parallel(callback: CallbackQuery, state: FSMContext):
    await state.update_data(parallel=int(callback.data.replace("grade_", "")))

    await callback.message.edit_text(text="Спасибо👍✅")
    await callback.message.answer(text=ASK_FRIEND_REQUEST)

    await callback.answer()

    await state.set_state(LoginForum.brawl_id)

@router.message(LoginForum.parallel)
async def wrong_parallel_format(message: Message):
    await message.answer(text="Пожайлуста, выберите свою парарель")

@router.message(LoginForum.brawl_id, F.text, BrawlStarsLinkFilter())
async def get_brawl_id(message: Message, state: FSMContext):
    await state.update_data(invite=[item.extract_from(message.text) for item in message.entities][0])

    data = await state.get_data()
    await message.answer(
        text=f"Name: {data["name"]}\nParallel: {data["parallel"]}\nPhone number: {data["phone"]}",
        reply_markup=get_aprovee()
    )

@router.message(LoginForum.brawl_id)
async def not_finded(message: Message):
    await message.answer(text="<b>Сыллка не найдена🫤</b>")
# get user group
@router.callback_query(F.data == "done")
async def save(
    callback: CallbackQuery,
    state: FSMContext
):
    db = BS_DB()
    data = await state.get_data()

    result = db.save_data(
        user_id=callback.from_user.id,
        name=data["name"],
        parallel=data["parallel"],
        phone_number=data["phone"],
        invite_link=data["invite"]
    )
    if result:
        await callback.message.delete()
        await callback.message.answer(text="<b>Выберите доступные опции</b>", reply_markup=options_keyboard()) #reply_markup=options_keyboard())
        
        await state.clear()
    else:
        await callback.message.edit_text(text="<b>Ошибка в регистрации...\n\nПопробуйте заново</b>")
        await callback.message.answer(text=ASK_NAME)
        await state.set_state(LoginForum.full_name)
    
    await callback.answer()

@router.callback_query(F.data == "edit")
async def restart(
    callback: CallbackQuery,
    state: FSMContext
):

    await callback.message.edit_text(text=ASK_NAME)

    await state.set_state(LoginForum.full_name)
    await callback.answer()

@router.message(Command('cancel'))
async def cancel(message: Message, state: FSMContext):
    await message.answer("States cleared")
    await state.clear()