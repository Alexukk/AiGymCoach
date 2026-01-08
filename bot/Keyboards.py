from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from trainigList import *

mainENkb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Trainings"), KeyboardButton(text="Music")],
    [KeyboardButton(text="Info")]
])



musicENKb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Get suggested music")],
    [KeyboardButton(text="Playlists")]
], one_time_keyboard=True)

confirmENKb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="✅Confirm✅"), KeyboardButton(text="❌Cancel❌")]
], one_time_keyboard=True, input_field_placeholder="Confirm or Cancel music suggestion")

durationKb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="30"), KeyboardButton(text="45"), KeyboardButton(text="60")],
    [KeyboardButton(text="90"), KeyboardButton(text="120")]
])


async def trainingsKbEn():
    kb = InlineKeyboardBuilder()
    for key, val in TRAININGS_INFO.items():
        kb.add(InlineKeyboardButton(text=val, callback_data=f"training:{key}"))
    return kb.adjust(2).as_markup()

