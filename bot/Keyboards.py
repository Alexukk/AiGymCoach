from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


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