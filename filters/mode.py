from aiogram.types import CallbackQuery
from aiogram.filters import BaseFilter
from database.BS import BS_DB

class Solo(BaseFilter):
    def __init__(self):
        self.db = BS_DB()


    async def __call__(self, callback: CallbackQuery):
        res = self.db.is_user_solo(callback.from_user.id)

        return res
    
class Duo(BaseFilter):
    def __init__(self):
        self.db = BS_DB()


    async def __call__(self, callback: CallbackQuery):
        res = self.db.is_user_duo(callback.from_user.id)

        return res
