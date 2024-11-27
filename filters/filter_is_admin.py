from aiogram.types import Message
from aiogram.filters import BaseFilter
from database.BS import BS_DB

class IsUserAdmin(BaseFilter):
    async def __call__(self, message: Message):
        db = BS_DB()
        
        return db.is_user_admin(message.from_user.id)  
        
    