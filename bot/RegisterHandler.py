from  aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from FSM import Register
from Database.requests import *
from bot.Keyboards import mainENkb

router = Router()



@router.message(F.text == "Register")
async def register_start(message, state: FSMContext):
    await state.set_state(Register.weight)
    await message.answer("Enter your weight <b>kg</b>:", parse_mode='HTML')

@router.message(Register.weight)
async def register_weight(message, state: FSMContext):
    await state.update_data(weight=message.text)
    await state.set_state(Register.height)
    await message.answer("Enter your height in <b>cm</b>:", parse_mode='HTML')


@router.message(Register.height)
async def register_age(message, state: FSMContext):
    await state.update_data(height=message.text)
    await state.set_state(Register.age)
    await message.answer("Enter your <b>valid age</b>, this is needed for better personalization: ",
                         parse_mode='HTML')

@router.message(Register.age)
async def register_age(message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.experience)
    await message.answer("Now enter your experience in <b>month</b>", parse_mode='HTML')

@router.message(Register.experience)
async def register_injuries(message, state: FSMContext):
    await state.update_data(experience=message.text)
    await state.set_state(Register.injuries)
    await message.answer("Enter your <b>injuries or limitations</b> as <i>pains, traumas and else.</i>", parse_mode='HTML')

@router.message(Register.injuries)
async def register_injuries(message, state: FSMContext):
    await state.update_data(injuries=message.text)
    await state.set_state(Register.description)
    await message.answer("Now enter <b>details</b> about you that might be useful for plan generation,"
                        " <i>preferences, loved exersice etc.</i>", parse_mode='HTML')


@router.message(Register.description)
async def register_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    data = await state.get_data()
    user_lang = message.from_user.language_code
    data['language'] = user_lang

    try:
        await set_user(message.from_user.id, data)
        await message.answer("<b>Success!</b> Your profile is saved.", parse_mode='HTML', reply_markup=mainENkb)
    except Exception as e:
        await message.answer("Something went wrong during saving...", reply_markup=mainENkb)
        print(f"Error: {e}")

    await state.clear()