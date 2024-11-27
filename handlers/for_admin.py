from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from filters.chat_filter import ChatTypeFIlter
from filters.filter_is_admin import IsUserAdmin

from keyboards.get_audience import get_audience_keyboard
from keyboards.get_admin_aprove import get_admin_aprove_keyboard
from keyboards.add_admin_photo import add_photo


from keyboards.main_funcktions import options_keyboard
from aiogram.fsm.state import  State, StatesGroup



from database.BS import BS_DB
import asyncio
import run

from constants import  ASKING_TEXT \
, USER_TEXT, ASKING_MEDIA, WRONG_FILE_TYPE, NEW_MESSAGE \
, MESSAGE_SUCCESSFULLY

from forums.NewsLetter import ForumNewsLetter

router = Router()


router.message.filter(ChatTypeFIlter("private"))


@router.message(IsUserAdmin(), Command("count"))
async def count_us(message: Message):
    db = BS_DB()
    await message.answer(text=str(db.count_users()[0]))


async def show_user_info(message: Message, mode, content):
    await message.answer(text=f"NAME: <b>{content[0]}</b>\nPHONE: <b>{content[1]}</b>\nPARALLEL: <b>{content[2]}</b>\nBS_INVITE: <b>{content[3]}</b>\nMode: <b>{mode}</b>", disable_web_page_preview=True)
    await asyncio.sleep(0.1)

@router.message(IsUserAdmin(), Command("solo"))
async def show_solo_players(message: Message):
    db = BS_DB()
    users = db.solo_players_info()

    await message.answer(text=f"All solo playres count - {users[0]}")
    
    if users[0] != 0:
        for user in users[1]:
            
            await show_user_info(message=message, mode="SOLO", content=user)

@router.message(IsUserAdmin(), Command("duo"))
async def show_duo_players(message: Message):
    db = BS_DB()
    users = db.duo_players_info()


    await message.answer(text=f"All duo players count - {users[0]}")
    
    if users[0] != 0:    
        for user in users[1]:
            
            await show_user_info(message=message, mode="DUO", content=user)
    




@router.message(IsUserAdmin(), Command("announcment"))
async def newsletter_send_all(message: Message, state: FSMContext):
    await message.answer(text=ASKING_TEXT)

    await state.set_state(ForumNewsLetter.asking_message_text)

@router.message(Command("announcment"))
async def user_not_admin(message: Message):
    await message.answer(text="<b>Это команда доступна только админам!</b>")

@router.message(ForumNewsLetter.asking_message_text, F.text)
async def is_ready(message: Message, state: FSMContext):
    await state.update_data(content=message.html_text)
    await message.answer(text=USER_TEXT.format(message.html_text), reply_markup=add_photo())

@router.callback_query(F.data == "photo")
async def adding_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=ASKING_MEDIA)
    await state.set_state(ForumNewsLetter.asking_message_media)

@router.callback_query(F.data == "move")
async def continue_process(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=USER_TEXT.format((await state.get_data())["content"]),
        reply_markup=get_admin_aprove_keyboard()
    )

    await state.set_state(ForumNewsLetter.asking_message_aprove)

@router.message(ForumNewsLetter.asking_message_media, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer_photo(
        photo=message.photo[-1].file_id,
        caption=USER_TEXT.format((await state.get_data())["content"]),
        reply_markup=get_admin_aprove_keyboard()
    )
    await state.set_state(ForumNewsLetter.asking_message_aprove)

@router.message(ForumNewsLetter.asking_message_media, F.video)
async def handle_video(message: Message, state: FSMContext):
    await state.update_data(video=message.video.file_id)
    await message.answer_video(
        video=message.video.file_id,
        caption=USER_TEXT.format((await state.get_data())["content"]),
        reply_markup=get_admin_aprove_keyboard()
    )
    await state.set_state(ForumNewsLetter.asking_message_aprove)

@router.message(ForumNewsLetter.asking_message_media)
async def not_media(message: Message):
    await message.answer(text=WRONG_FILE_TYPE)

@router.callback_query(ForumNewsLetter.asking_message_aprove, F.data == "yeah")
async def send_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    db = BS_DB()
    users = db.fetchall_users()
    state_data = await state.get_data()

    async def send_message_to_user(user):
        user_id = int(user[0])
        try:
            if (await state.get_data()).get("photo", None) is not None:
                await run.bot.send_photo(chat_id=user_id, photo=(await state.get_data())["photo"], caption=NEW_MESSAGE.format(state_data["content"]))
            elif (await state.get_data()).get("video", None) is not None:
                await run.bot.send_video(chat_id=user_id, video=(await state.get_data())["video"], caption=NEW_MESSAGE.format(state_data["content"]))
            else:
                await run.bot.send_message(chat_id=user_id, text=NEW_MESSAGE.format(state_data["content"]))
            return 1
        except TelegramForbiddenError:
            print(f"[INFO] User {user_id} blocked the bot")
            return 0
        except Exception as e:
            print(f"[ERROR] Failed to send message to user {user_id}: {e}")
            return 0

    tasks = [send_message_to_user(user) for user in users]
    count = sum(await asyncio.gather(*tasks))

    print(f"[INFO] {count} users received the message")

    try:
        print(f"[INFO] {callback.from_user.id} sent message")
        await callback.message.answer(text=MESSAGE_SUCCESSFULLY)    
    except TelegramBadRequest:
        pass

    await state.clear()

@router.callback_query(ForumNewsLetter.asking_message_aprove, F.data == "nuh")
async def not_approved(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(text=ASKING_TEXT)
    except TelegramBadRequest:
        pass
    await callback.answer()
    await state.set_state(ForumNewsLetter.asking_message_text)

# class AdminRightsForum(StatesGroup):
#     id = State()

# @router.message(Command("admin"))
# async def giv_admin(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer(text="type an person id  to give him an admin rights")
#     await state.set_state(AdminRightsForum.id)

# @router.message(AdminRightsForum.id, F.text)
# async def give_admin_rights(message: Message, state: FSMContext):
#     db = NisDB()
#     db.give_admin(user_id=int(message.text.split()[0]), admin=int(message.text.split()[1]))
#     await message.answer(text="succes!")
#     await state.clear()


# class AdminRightsForum(StatesGroup):
#     id = State()

# @router.message(Command("newadmin"),IsUserAdmin())
# async def giv_admin(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer(text="type an person id  to give him an admin rights")
#     await state.set_state(AdminRightsForum.id)

# @router.message(AdminRightsForum.id, F.text)
# async def give_admin_rights(message: Message, state: FSMContext):
#     db = NisDB()
#     db.give_admin(user_id=int(message.text.split()[0]), admin=int(message.text.split()[1]))
#     await message.answer(text="succes!")
#     await state.clear()