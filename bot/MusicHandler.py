from  aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from Keyboards import *


router = Router()


@router.message(F.text == "Music")
async def music_menu(message: Message):
    await message.answer("<b>Music</b>\n"
                         "Wanna get list of all playlists? \n"
                         "Or wanna get suggestion based on your mood?"
                         "Choose between options below")