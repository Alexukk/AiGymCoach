from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


mainENkb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Trainings"), KeyboardButton(text="Music")],
    [KeyboardButton(text="Info")]
])