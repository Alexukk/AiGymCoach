from  aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from Keyboards import *
from bot.FSM import GetPersonalPlan
from trainigList import TRAININGS_INFO
from TrainingsRequestsAPI import Get_Training_plan


router = Router()

@router.message(F.text == "Trainings")
async def trainings_start(message: Message):
    await message.answer("<b>Choose a muscle group to proceed</b>",
                     parse_mode='HTML', reply_markup=await trainingsKbEn())


@router.callback_query(F.data.startswith("training:"))
async def start_muscle(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        await callback.message.edit_reply_markup(reply_markup=None)

    group_id = int(callback.data.split(":")[1])
    muscle_name = TRAININGS_INFO[group_id]

    await state.set_state(GetPersonalPlan.feelings)
    await state.update_data(muscle_group=muscle_name)

    await callback.message.answer(
        "<b>🏋️ NEW TRAINING SESSION</b>\n"
        f"Target: <code>{muscle_name.upper()}</code>\n\n"
        "<b>Step 1:</b> Describe your mood, energy level, and injuries:",
        parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(GetPersonalPlan.feelings)
async def get_feelings(message: Message, state: FSMContext):
    await state.update_data(feelings=message.text)
    await state.set_state(GetPersonalPlan.duration)
    await message.answer(
        "<b>Step 2:</b> Choose duration (minutes) by buttons or enter a number:",
        reply_markup=durationKb,
        parse_mode='HTML'
    )


@router.message(GetPersonalPlan.duration)
async def get_duration(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Please enter a valid number (e.g. 45)")
        return

    await state.update_data(duration=message.text)
    await state.set_state(GetPersonalPlan.confirm)

    data = await state.get_data()

    text = (
        "<b>📋 Review Your Request</b>\n"
        "───────────────────\n"
        f"<b>💪 Muscle:</b> <code>{data['muscle_group']}</code>\n"
        f"<b>⏱️ Duration:</b> <code>{data['duration']} min</code>\n"
        f"<b>🧘 State:</b> <i>{data['feelings']}</i>\n"
        "───────────────────\n"
        "Confirm to proceed:"
    )

    await message.answer(text, reply_markup=confirmENKb, parse_mode='HTML')


@router.message(GetPersonalPlan.confirm)
async def confirm_plan_request(message: Message, state: FSMContext):
    if message.text == "✅Confirm✅":
        data = await state.get_data()

        status_msg = await message.answer("⏳ <i>AI is composing your training plan...</i>",
                                          parse_mode='HTML',
                                          reply_markup=ReplyKeyboardRemove())

        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            AI_RESPONSE = await Get_Training_plan(
                user_text=data["feelings"],
                group=data["muscle_group"],
                duration=data["duration"]
            )

        await status_msg.delete()
        await message.answer(AI_RESPONSE, reply_markup=mainENkb, parse_mode='HTML')
        await state.clear()
        await message.answer("<b>Workout plan is ready</b>, what about getting suggestion on music for training?\n"
                             "press button 'Music' and get your suggestion.", parse_mode='HTML')
        return

    await state.clear()
    await message.answer("<b>Canceled</b>", reply_markup=mainENkb, parse_mode='HTML')
