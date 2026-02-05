from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


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




async def Inline_Builder(data: dict, utils: str, prefix: str):
    builder = InlineKeyboardBuilder()
    for text, column in data.items():
        builder.add(InlineKeyboardButton(
            text=f"{utils} {text}",
            callback_data=f"{prefix}{column}")
        )

    builder.adjust(2)
    return builder.as_markup()


async def Reply_Builder(buttons: list):
    builder = ReplyKeyboardBuilder()
    for i in buttons:
        builder.add(KeyboardButton(text=i))

    builder.adjust(2)
    return  builder.as_markup()
