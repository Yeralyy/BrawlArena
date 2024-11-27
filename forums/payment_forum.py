from aiogram.fsm.state import State, StatesGroup

class PaymentForum(StatesGroup):
    name = State()
    wait_buy = State()
    