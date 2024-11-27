from aiogram import Router, F

from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext

from filters.is_user_in_db import IsUserInDB
from filters.chat_filter import ChatTypeFIlter 
from filters.mode import Solo, Duo

from aiogram.filters import CommandStart, Command

from keyboards.ask_compite import get_compit
from keyboards.chose_mode import get_mode
from keyboards.buy_ticket import buy_ticket_duo, buy_ticket_solo, verify, payment 

from constants import TOURAMENT_INFO, SOLO_INFO, DUO_INFO, ASK_NAME_TICKET, \
BUY_TICKET_SOLO, BUY_TICKET_DUO, VERIFY, WAIT_VERYFING, MESSAGE_USER_NOT_VERYFIED, MESSAGE_USER_VERYFIED

from forums.payment_forum import PaymentForum

import run

from database.BS import BS_DB

router = Router()

router.message.filter(
    ChatTypeFIlter("private")
)

router.message.filter(
    IsUserInDB()
)

@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Состояние отменено!')

@router.message(F.text=="125 High School Tourament🏆")
async def tourament(message: Message, state: FSMContext):
    await message.answer(text=TOURAMENT_INFO
, reply_markup=get_mode())

@router.callback_query(F.data == "mode_solo", Solo())
async def solo_in(callback: CallbackQuery):
    await callback.message.edit_text(text="<b>Вы уже участвуете в СОЛО ШД!😼</b>")

@router.callback_query(F.data == "mode_solo")
async def solo_mode_info(callback: CallbackQuery):
    await callback.message.edit_text(text=SOLO_INFO, reply_markup=buy_ticket_solo())

@router.callback_query(F.data == "mode_duo", Duo())
async def duo_in(callback: CallbackQuery):
    await callback.message.edit_text(text="<b>Вы уже участвуете в ДУО ШД!😼</b>")



@router.callback_query(F.data == "mode_duo")
async def duo_mode_info(callback: CallbackQuery):
    await callback.message.edit_text(text=DUO_INFO, reply_markup=buy_ticket_duo())



@router.callback_query(F.data == "buy_solo")
async def wait_payment_solo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=ASK_NAME_TICKET)
    await state.update_data(solo=True)

    await state.set_state(PaymentForum.name)

@router.callback_query(F.data == "buy_duo")
async def wait_payment_duo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=ASK_NAME_TICKET)
    await state.update_data(duo=True)

    await state.set_state(PaymentForum.name)

@router.message(F.text, PaymentForum.name)
async def give_reckvo(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await state.update_data(buy_name=message.text)

    if state_data.get("solo", False):

        await message.answer(text=BUY_TICKET_SOLO + "\n\nНажмите на номер карты, чтобы его скопировать🤳🏻⬆️", reply_markup=verify())
    elif state_data.get("duo", False):
        await message.answer(text=BUY_TICKET_DUO + "\n\nНажмите на номер карты, чтобы его скопировать🤳🏻⬆️", reply_markup=verify())
    
    await state.set_state(PaymentForum.wait_buy)

@router.callback_query(PaymentForum.wait_buy, F.data == "bought")
async def verify_payment(callback: CallbackQuery, state: FSMContext):
    
    state_data = await state.get_data()
    if state_data.get("solo", False):

        await run.bot.send_message(chat_id=5686783384,  text=VERIFY.format(state_data["buy_name"], "SOLO"), reply_markup=payment(callback.from_user.id, "solo"))
        await run.bot.send_message(chat_id=6407797400,  text=VERIFY.format(state_data["buy_name"], "SOLO"), reply_markup=payment(callback.from_user.id, "solo"))
    else:

        await run.bot.send_message(chat_id=5686783384,  text=VERIFY.format(state_data["buy_name"], "DUO"), reply_markup=payment(callback.from_user.id, "duo"))
        await run.bot.send_message(chat_id=6407797400,  text=VERIFY.format(state_data["buy_name"], "DUO"), reply_markup=payment(callback.from_user.id, "duo"))

    await callback.message.edit_text(text=WAIT_VERYFING)
    await state.clear()

@router.callback_query(F.data.startswith("yesv_"))
async def verified(callback: CallbackQuery):
    await callback.message.edit_text(text="<b>Расталды😌</b>")
    db = BS_DB()

    cb_data = callback.data.replace("yesv_", "").split("_")

    

    db.save_user_mode(user_id=int(cb_data[0]), mode=cb_data[1])


    await run.bot.send_message(chat_id=int(cb_data[0]), text=MESSAGE_USER_VERYFIED)

@router.callback_query(F.data.startswith("notv_"))
async def verified(callback: CallbackQuery):
    await callback.message.edit_text(text="<b>Расталмады😢</b>")

    cb_data = callback.data.replace("notv_", "").split("_")

    await run.bot.send_message(chat_id=int(cb_data[0]), text=MESSAGE_USER_NOT_VERYFIED)
