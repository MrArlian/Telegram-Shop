import asyncio

from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types, executor

from modules import Settings


bot = Bot(Settings.TelegramToken, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
storage = RedisStorage2(Settings.Host, Settings.Port, db=3, password=Settings.Password)
dispatcher = Dispatcher(bot, storage=storage)


def main() -> None:
    from handlers.middleware import CheckAdminRole
    from handlers import dispatcher as dp
    from loop import task

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    dp.setup_middleware(CheckAdminRole())

    loop.create_task(task())

    try:
        executor.start_polling(dp, loop=loop)
    finally:
        loop.run_until_complete(dp.storage.close())
        loop.run_until_complete(dp.storage.wait_closed())


if __name__ == '__main__':
    main()
