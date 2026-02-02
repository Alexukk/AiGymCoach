from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from Keyboards import *
from Database.requests import get_user_data
from aiogram.fsm.context import FSMContext
from FSM import EditProfile
from Database.requests import update_user_field
from LanguageUtils import get_text, get_user_details, get_user_langcode
from bot.Database.requests import get_user_language
from bot.LanguageUtils import get_keyboard
from bot.Texts.ProfileTexts import PROFILE_TEXTS, ADDITIVES_TEXTS

router = Router()


@router.message(F.text == "👤 My Profile")
async def show_profile(message: Message):
    user_data = await get_user_data(message.from_user.id)
    u_details = await get_user_details(message)
    lang = await get_text(u_details, "get_lang_only", {"get_lang_only": {"uk": "uk", "en": "en"}})

    if not user_data:
        return await message.answer(await get_text(u_details, "not_registered", PROFILE_TEXTS), parse_mode='HTML')


    f = PROFILE_TEXTS["fields"]
    m_unit = PROFILE_TEXTS["unit_month"][lang]

    profile_text = (
        f"{PROFILE_TEXTS['profile_header'][lang]}"
        f"{f['weight'][lang]}: {user_data.weight} kg\n"
        f"{f['height'][lang]}: {user_data.height} cm\n"
        f"{f['age'][lang]}: {user_data.age}\n"
        f"{f['experience'][lang]}: {user_data.experience} {m_unit}\n"
        f"{f['injuries'][lang]}: {user_data.injuries or PROFILE_TEXTS['none'][lang]}\n"
        f"{f['description'][lang]}: {user_data.description or PROFILE_TEXTS['empty'][lang]}\n"
        f"{f['language'][lang]}: {'🇺🇦 Ukrainian' if user_data.language == 'uk' else '🇺🇸 English'}\n"
        f"{PROFILE_TEXTS['footer'][lang]}"
    )
    await message.answer(profile_text, reply_markup=await get_keyboard("edit_profile",
                                                                       await get_user_langcode(message.from_user)), parse_mode='HTML')
    return None


@router.callback_query(F.data.startswith("change_"))
async def start_edit_field(callback: CallbackQuery, state: FSMContext):
    column_name = callback.data.split("_")[1]
    u_details = await get_user_details(callback)
    lang = await get_text(u_details, "get_lang_only", {"get_lang_only": {"uk": "uk", "en": "en"}})

    await state.update_data(editing_column=column_name)
    await state.set_state(EditProfile.waiting_for_value)

    if column_name.lower() == "language":
        await callback.message.answer(PROFILE_TEXTS["choose_lang"][lang], reply_markup=languageKB)
        return

    field_name = PROFILE_TEXTS["fields"][column_name][lang]
    additive = ADDITIVES_TEXTS[column_name][lang]

    prompt = PROFILE_TEXTS["enter_new_value"][lang].format(field=field_name, additive=additive)

    await callback.message.answer(prompt, parse_mode='HTML')
    await callback.answer()


@router.message(EditProfile.waiting_for_value)
async def save_edited_value(message: Message, state: FSMContext):
    data = await state.get_data()
    column_name = data.get("editing_column")
    u_details = await get_user_details(message)

    new_value = message.text
    if new_value == "🇺🇸":
        new_value = "en"
    elif new_value == "🇺🇦":
        new_value = "uk"

    await update_user_field(message.from_user.id, column_name, new_value)

    # Получаем финальный текст подтверждения
    lang = await get_text(u_details, "get_lang_only", {"get_lang_only": {"uk": "uk", "en": "en"}})
    field_name = PROFILE_TEXTS["fields"][column_name][lang]
    success_msg = PROFILE_TEXTS["update_success"][lang].format(field=field_name)

    await state.clear()
    await message.answer(success_msg, reply_markup=mainENkb)