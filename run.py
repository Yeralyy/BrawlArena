from aiogram     import Dispatcher
import asyncio
import CONFIG
import logging


from aiogram.fsm.storage.redis import RedisStorage

from handlers import login, typical_handler, touraments, for_admin

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s"
)


storage = RedisStorage.from_url("redis://127.0.0.1:6379")

dp = Dispatcher(storage=storage)
bot = CONFIG.bot



async def main():
    dp.include_router(typical_handler.router)
    dp.include_router(touraments.router)
    dp.include_router(for_admin.router)
    dp.include_router(login.router)


    await dp.start_polling(bot)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Keyboard interrupt")


