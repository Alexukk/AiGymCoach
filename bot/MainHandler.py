from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from Keyboards import *
from LanguageUtils  import get_text, get_user_details
from bot.Texts.MainTexts import MAIN_HANDLER_TEXT
router = Router()







@router.message(CommandStart())
async def start(message: Message):
    await message.reply( await get_text(await get_user_details(message),"Greetings", MAIN_HANDLER_TEXT),
                        reply_markup=mainENkb,
                        parse_mode='HTML')


@router.message(F.text == "ℹ️ Info")
async def info(message: Message):
    await message.reply(await get_text(await get_user_details(message), "Info", MAIN_HANDLER_TEXT)
        ,
        parse_mode='HTML',
        disable_web_page_preview=True
    )