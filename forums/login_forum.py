from aiogram.fsm.state import State, StatesGroup

class LoginForum(StatesGroup):
    full_name = State()
    phone_number = State()
    parallel = State()
    brawl_id = State()
