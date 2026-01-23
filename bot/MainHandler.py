from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from Keyboards import *
from Database.requests import get_user_language
from MainTexts import MAIN_MK_TEXT
router = Router()



async def get_text(tg_id, text_details, user_lang):
    lang_from_db = await get_user_language(tg_id)
    final_lang = lang_from_db if lang_from_db else user_lang

    if final_lang == "ru":
        final_lang = "uk"

    if final_lang not in ["en", "uk"]:
        final_lang = "en"

    target_dict = MAIN_MK_TEXT.get(text_details, {})
    return target_dict.get(final_lang, target_dict.get(final_lang, "Error: Text not found"))





@router.message(CommandStart())
async def start(message: Message):
    await message.reply( await get_text(message.from_user.id,"Greetings", message.from_user.language_code),
                        reply_markup=mainENkb,
                        parse_mode='HTML')


@router.message(F.text == "ℹ️ Info")
async def info(message: Message):
    await message.reply(await get_text(message.from_user.id,"Info", message.from_user.language_code)
        ,
        parse_mode='HTML',
        disable_web_page_preview=True
    )