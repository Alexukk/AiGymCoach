from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from Keyboards import *
from LanguageUtils  import get_text, get_user_details
from bot.Texts.MainTexts import MAIN_HANDLER_TEXT
from LanguageUtils import get_keyboard, get_user_langcode
router = Router()







@router.message(CommandStart())
async def start(message: Message):
    await message.reply( await get_text(await get_user_details(message),"Greetings", MAIN_HANDLER_TEXT),
                        reply_markup=await get_keyboard("MainMenu",
                        await get_user_langcode(message.from_user)),
                        parse_mode='HTML')


@router.message(F.text.in_({"ℹ️ Info", "ℹ️ Інформація"}))
async def info(message: Message):
    await message.reply(await get_text(await get_user_details(message), "Info", MAIN_HANDLER_TEXT)
        ,
        parse_mode='HTML',
        disable_web_page_preview=True
    )