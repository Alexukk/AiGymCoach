from  aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from Keyboards import *
from bot.FSM import GetPersonalPlan
from trainigList import TRAININGS_INFO


router = Router()

@router.message(F.text == "Trainings")
async def trainings_start(message: Message):
    await message.answer("<b>Choose a muscle group to proceed</b>", parse_mode='HTML', reply_markup=await trainingsKbEn())


@router.callback_query(F.data.startswith("training:"))
async def start_muscle(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    try:
        await callback.message.delete()
    except TelegramBadRequest:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception as e:
        print(f"Couldn't delete the message: {e}")

    group_id = int(callback.data.split(":")[1])
    muscle_name = TRAININGS_INFO[group_id]

    await state.set_state(GetPersonalPlan.feelings)
    await state.update_data(muscle_group=muscle_name)

    await callback.message.answer(
        "<b>🏋️ NEW TRAINING SESSION</b>\n"
        "───────────────────\n"
        f"<b>Target Muscle:</b> <code>{muscle_name.upper()}</code>\n\n"
        "<b>What I need from you:</b>\n"
        "Tell me about your current <b>mood</b>, <b>energy level</b>, and any <b>physical limits</b> or injuries.\n\n"
        "<b>💡 Example:</b>\n"
        "<i>«Feeling great and motivated, but I have a slight pain in my left wrist, so avoid heavy presses.»</i>\n"
        "───────────────────\n"
        "<b>✍️ Waiting for your description...</b>",
        parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(GetPersonalPlan.feelings)
async def get_feelings(message, state: FSMContext):
    await state.update_data(feelings=message.text)
    await state.set_state(GetPersonalPlan.confirm)
    data = await state.get_data()
    muscle = data.get('muscle_group', 'Not selected')
    feelings = data.get('feelings', 'No description')

    text = (
        "<b>📋 Review Your Training Request</b>\n"
        "───────────────────\n"
        f"<b>💪 Muscle Group:</b> <code>{muscle}</code>\n"
        f"<b>🧘 Your State:</b>\n<i>«{feelings}»</i>\n"
        "───────────────────\n"
        "<i>If everything is correct, press <b>Confirm</b>.\n"
        "Otherwise, <b>Cancel</b> to start over.</i>"
    )

    await message.answer(
        text,
        reply_markup=confirmENKb,
        parse_mode='HTML'
    )