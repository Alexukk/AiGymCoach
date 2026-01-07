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
        f"<b>Target: {muscle_name}</b>\n\n"
        f"Please describe your feelings, mood, energy level, and any health limits.\n"
        f"<i>Example: 'Feeling energetic, but have a slight pain in my left wrist.'</i>",
        parse_mode='HTML', reply_markup=ReplyKeyboardRemove()
    )


@router.message(GetPersonalPlan.feelings)
async def get_feelings(message, state: FSMContext):
    user_feelings = message.text
    await state.set_state(GetPersonalPlan.confirm)
    await state.update_data(feelings=user_feelings)

    await message.answer(f"<b>Now check all details:</b>\n"
                         f"<b>Muscle group: {await state.get_value('muscle_group')}</b>"
                         f"Your feelings: \n"
                         f"<i>{await state.get_value('feelings')}</i>\n"
                         f"If everything fine Confirm and proceed in other case Cancel and start from a scratch",
                         reply_keyboard=confirmENKb, parse_mode='HTML')

