from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from trainigList import *

mainENkb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🏋️‍♀️ Trainings"), KeyboardButton(text="🎧 Music")],
    [KeyboardButton(text="ℹ️ Info"), KeyboardButton(text="👤 My Profile")]
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

languageKB = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🇺🇦")], [KeyboardButton(text='🇺🇸')]
])

async def trainingsKbEn():
    kb = InlineKeyboardBuilder()
    for key, val in TRAININGS_INFO.items():
        kb.add(InlineKeyboardButton(text=val, callback_data=f"training:{key}"))
    return kb.adjust(2).as_markup()


def edit_profile_kb():
    builder = InlineKeyboardBuilder()

    fields = {
        "Weight": "weight",
        "Height": "height",
        "Age": "age",
        "Experience": "experience",
        "Injuries": "injuries",
        "Description": "description",
        "Language": "language",
    }

    for text, column in fields.items():
        builder.add(InlineKeyboardButton(
            text=f"Edit {text}",
            callback_data=f"change_{column}")
        )

    builder.adjust(2)
    return builder.as_markup()
