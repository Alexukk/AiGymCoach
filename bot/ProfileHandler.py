from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from Keyboards import *
from Database.requests import get_user_data
from aiogram.fsm.context import FSMContext
from FSM import EditProfile
from Database.requests import update_user_field

router = Router()

message_additivesEN = {
        "weight": "in kg",
        "height": "in cm",
        "age": "in years",
        "experience": "in month",
        "injuries": "Describe all of them with as much details as possible",
        "description": "Enter all details about you which will help bot improve it's answers",
        "language": "use EN for english, ES for spanish",
}



@router.message(F.text == "👤 My Profile")
async def show_profile(message: Message):
    user_data = await get_user_data(message.from_user.id)

    if not user_data:
        return await message.answer("You are not registered yet. Enter <code>Register</code>")

    profile_text = (
        f"<b>Your Fitness Profile</b>\n\n"
        f"⚖️ <b>Weight:</b> {user_data.weight} kg\n"
        f"📏 <b>Height:</b> {user_data.height} cm\n"
        f"🎂 <b>Age:</b> {user_data.age}\n"
        f"🏅 <b>Experience:</b> {user_data.experience} month\n"
        f"🤕 <b>Injuries:</b> {user_data.injuries or 'None'}\n"
        f"📝 <b>Bio:</b> {user_data.description or 'Empty'}\n"
        f"🌐 <b>Language:</b> {'🇺🇦 Ukrainian' if user_data.language == 'uk' else '🇺🇸 English'}\n\n"
        f"<i>Select a button below to update your information:</i>"
    )

    await message.answer(profile_text, reply_markup=edit_profile_kb(), parse_mode='HTML')


@router.callback_query(F.data.startswith("change_"))
async def start_edit_field(callback: CallbackQuery, state: FSMContext):
    column_name = callback.data.split("_")[1]


    await state.update_data(editing_column=column_name)
    await state.set_state(EditProfile.waiting_for_value)

    if column_name.lower() == "language":
        await callback.message.answer(f"Choose an option below:", reply_markup=languageKB)
        return

    await callback.message.answer(f"Enter new value for <b>{column_name} </b>{message_additivesEN[column_name]}:", parse_mode='HTML')
    await callback.answer()


@router.message(EditProfile.waiting_for_value)
async def save_edited_value(message: Message, state: FSMContext):
    user_data = await state.get_data()
    column_name = user_data.get("editing_column")
    new_value = message.text

    if message.text == "🇺🇸":
            mew_value="en"
    elif message.text == "🇺🇦":
        new_value="uk"


    await update_user_field(message.from_user.id, column_name, new_value)

    await state.clear()
    await message.answer(f"✅ Your {column_name} has been updated!", reply_markup=mainENkb)