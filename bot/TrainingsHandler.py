from  aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from Database.requests import get_user_data

from Keyboards import *
from bot.Database.requests import get_user_language
from bot.FSM import GetPersonalPlan
from TrainingsRequestsAPI import Get_Training_plan
from LanguageUtils import get_text, get_user_details, get_user_langcode, get_keyboard
from bot.Texts.TrainingsText import TRAININGS_LEXICON
from KeyboardsDICTS import get_TRAININGS


router = Router()



@router.message(F.text == "🏋️‍♀️ Trainings")
async def trainings_start(message: Message):
    u_details = await get_user_details(message)
    text = await get_text(u_details, "choose_group", TRAININGS_LEXICON)

    await message.answer(text, reply_markup=await get_keyboard("muscle_group",
                                                                       await get_user_langcode(message.from_user)), parse_mode='HTML')


@router.callback_query(F.data.startswith("training:"))
async def start_muscle(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    u_details = await get_user_details(callback)
    TRAININGS_INFO = get_TRAININGS(await get_user_langcode(callback.from_user))
    group_id = int(callback.data.split(":")[1])
    id_to_name = {v: k for k, v in TRAININGS_INFO.items()}
    muscle_name = id_to_name.get(str(group_id), "Unknown")
    await state.update_data(muscle_group=muscle_name)
    await state.set_state(GetPersonalPlan.feelings)

    template = await get_text(u_details, "new_session", TRAININGS_LEXICON)
    await callback.message.answer(
        template.format(muscle=muscle_name.upper()),
        parse_mode='HTML', reply_markup=ReplyKeyboardRemove()
    )


@router.message(GetPersonalPlan.feelings)
async def get_feelings(message: Message, state: FSMContext):
    await state.update_data(feelings=message.text)
    await state.set_state(GetPersonalPlan.duration)

    u_details = await get_user_details(message)
    text = await get_text(u_details, "choose_duration", TRAININGS_LEXICON)
    await message.answer(text, reply_markup=durationKb, parse_mode='HTML')


@router.message(GetPersonalPlan.duration)
async def get_duration(message: Message, state: FSMContext):
    u_details = await get_user_details(message)
    if not message.text.isdigit():
        text = await get_text(u_details, "invalid_number", TRAININGS_LEXICON)
        return await message.answer(text)

    await state.update_data(duration=message.text)
    await state.set_state(GetPersonalPlan.confirm)
    data = await state.get_data()

    template = await get_text(u_details, "review_request", TRAININGS_LEXICON)
    text = template.format(muscle=data['muscle_group'], duration=data['duration'], feelings=data['feelings'])
    await message.answer(text ,
                         reply_markup=await get_keyboard("Confirm", await get_user_langcode(message.from_user)),
                         parse_mode='HTML')
    return None


@router.message(GetPersonalPlan.confirm)
async def confirm_plan_request(message: Message, state: FSMContext):
    u_details = await get_user_details(message)

    if message.text == "✅Confirm✅" or message.text == "✅Підтвердити✅":
        data = await state.get_data()

        status_text = await get_text(u_details, "ai_composing", TRAININGS_LEXICON)
        status_msg = await message.answer(status_text, parse_mode='HTML', reply_markup=ReplyKeyboardRemove())

        user_db_data = await get_user_data(message.from_user.id)
        profile_context = "Not registered"
        if user_db_data:
            profile_context = f"Age: {user_db_data.age}, Weight: {user_db_data.weight}kg..."

        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            lang_code = await get_user_language(message.from_user.id)
            AI_RESPONSE = await Get_Training_plan(
                user_text=data["feelings"],
                group=data["muscle_group"],
                duration=data["duration"],
                user_profile=profile_context,
                language=lang_code
            )

        await status_msg.delete()
        await message.answer(AI_RESPONSE, reply_markup=await get_keyboard("MainMenu",
                        await get_user_langcode(message.from_user)), parse_mode='HTML')

        footer_text = await get_text(u_details, "ready_footer", TRAININGS_LEXICON)
        await message.answer(footer_text, parse_mode='HTML')
        await state.clear()
    else:
        cancel_text = await get_text(u_details, "canceled", TRAININGS_LEXICON)
        await message.answer(cancel_text, reply_markup=await get_keyboard("MainMenu",
                        await get_user_langcode(message.from_user)), parse_mode='HTML')
        await state.clear()