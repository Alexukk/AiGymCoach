from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from FSM import Register
from Database.requests import set_user
from bot.Keyboards import mainENkb  # Позже заменим на динамическую
from LanguageUtils import get_text, get_user_details
from bot.Texts.RegisterTexts import REGISTER_HANDLER_TEXT

router = Router()


@router.message(F.text == "Register")
async def register_start(message: Message, state: FSMContext):
    await state.set_state(Register.weight)
    text = await get_text(await get_user_details(message), "enter_weight", REGISTER_HANDLER_TEXT)
    await message.answer(text, parse_mode='HTML')


@router.message(Register.weight)
async def register_weight(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await state.set_state(Register.height)
    text = await get_text(await get_user_details(message), "enter_height", REGISTER_HANDLER_TEXT)
    await message.answer(text, parse_mode='HTML')


@router.message(Register.height)
async def register_height(message: Message, state: FSMContext):  # Исправил имя функции (было дублирование age)
    await state.update_data(height=message.text)
    await state.set_state(Register.age)
    text = await get_text(await get_user_details(message), "enter_age", REGISTER_HANDLER_TEXT)
    await message.answer(text, parse_mode='HTML')


@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.experience)
    text = await get_text(await get_user_details(message), "enter_experience", REGISTER_HANDLER_TEXT)
    await message.answer(text, parse_mode='HTML')


@router.message(Register.experience)
async def register_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await state.set_state(Register.injuries)
    text = await get_text(await get_user_details(message), "enter_injuries", REGISTER_HANDLER_TEXT)
    await message.answer(text, parse_mode='HTML')


@router.message(Register.injuries)
async def register_injuries(message: Message, state: FSMContext):
    await state.update_data(injuries=message.text)
    await state.set_state(Register.description)
    text = await get_text(await get_user_details(message), "enter_description", REGISTER_HANDLER_TEXT)
    await message.answer(text, parse_mode='HTML')


@router.message(Register.description)
async def register_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    data = await state.get_data()
    # Сохраняем язык системы как дефолтный при регистрации
    data['language'] = message.from_user.language_code

    u_details = await get_user_details(message)

    try:
        await set_user(message.from_user.id, data)
        success_text = await get_text(u_details, "register_success", REGISTER_HANDLER_TEXT)
        await message.answer(success_text, parse_mode='HTML', reply_markup=mainENkb)
    except Exception as e:
        error_text = await get_text(u_details, "register_error", REGISTER_HANDLER_TEXT)
        await message.answer(error_text, reply_markup=mainENkb)
        print(f"Error saving user: {e}")

    await state.clear()