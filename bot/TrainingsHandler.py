from  aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from Keyboards import *


router = Router()

@router.message(F.text == "Trainings")
async def trainings_start(message: Message):
    await message.answer("<b>Choose a muscle group to proceed</b>", parse_mode='HTML', reply_markup=await trainingsKbEn())