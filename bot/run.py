import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from MainHandler import router as router_main
from MusicHandler import router as router_music
from TrainingsHandler import router as router_trainings

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router_main)
    dp.include_router(router_music)
    dp.include_router(router_trainings)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
