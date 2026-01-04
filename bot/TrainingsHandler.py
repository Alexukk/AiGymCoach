from  aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

router = Router()


@router.message(CommandStart)
async def start(message: Message):
    await message.reply(f"<b>Hello user!</b>\n"
                        f"few commands you might need:"
                        f"1. Choose 'Info' button to get tutorial trough bot"
                        f"2. Choose 'Trainings' to get your personalized plan"
                        f"3. Choose 'Music' to get playlists based on your mood", parse_mode='HTML')