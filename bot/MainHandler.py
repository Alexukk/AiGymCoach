from pickle import FROZENSET

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from Keyboards import *
from Database.requests import get_user_language
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.reply(f"<b>Hello user!</b>\n"
                        f"<b>Please enter <code>Register</code> to fully register and get as personalized plan as possible</b>\n"
                        f"Or just proceed without registration."
                        f"few commands you might need:"
                        f"1. Choose 'Info' button to get tutorial trough bot\n"
                        f"2. Choose 'Trainings' to get your personalized plan\n"
                        f"3. Choose 'Music' to get playlists based on your mood\n",
                        reply_markup=mainENkb,
                        parse_mode='HTML')


@router.message(F.text == "ℹ️ Info")
async def info(message: Message):
    await message.reply(
        "<b>🦾 AI Training Assistant</b>\n\n"
        "<blockquote>Your personalized coach that listens to your mood. This app generates and adjusts training programs based on how you feel right now.</blockquote>\n\n"
        "<b>How it works:</b>\n"
        "1️⃣ Open <b>Trainings</b> in the main menu\n"
        "2️⃣ Select your <b>target muscle group</b>\n"
        "3️⃣ Describe your <b>mood & energy level</b>\n\n"
        "✨ <i>The AI will instantly craft a structured plan tailored just for you.</i>\n\n"
        "💎<i>If you want experience our bot's best abilities please complete registration by sending: <code>Register</code> to the bot and answering few questions</i>\n"
        "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        "<b>Powered by:</b> <a href='https://github.com/Alexukk'>Alexukk</a>",
        parse_mode='HTML',
        disable_web_page_preview=True
    )