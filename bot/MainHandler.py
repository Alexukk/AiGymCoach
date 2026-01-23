from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from Keyboards import *
from LanguageUtils  import get_text
from bot.Texts.MainTexts import MAIN_MK_TEXT
router = Router()







@router.message(CommandStart())
async def start(message: Message):
    await message.reply( await get_text(message.from_user.id,"Greetings", message.from_user.language_code, MAIN_MK_TEXT),
                        reply_markup=mainENkb,
                        parse_mode='HTML')


@router.message(F.text == "ℹ️ Info")
async def info(message: Message):
    await message.reply(await get_text(message.from_user.id,"Info", message.from_user.language_code, MAIN_MK_TEXT)
        ,
        parse_mode='HTML',
        disable_web_page_preview=True
    )