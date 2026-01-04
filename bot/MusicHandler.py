from  aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from Keyboards import *
from FSM import *
from RequestsAPI import *

router = Router()


@router.message(F.text == "Music")
async def music_menu(message: Message):
    await message.answer("<b>Music</b>\n"
                         "Wanna get list of all playlists? \n"
                         "Or wanna get suggestion based on your mood?"
                         "Choose between options below", reply_markup=musicENKb, parse_mode='HTML')


@router.message(F.text == "Playlists")
async def playlists(message: Message):
    await message.answer("Some text here with links..")


@router.message(F.text == "Get suggested music")
async def suggested_music(message, state: FSMContext):
    await state.set_state(SuggestMusic.text)
    await message.answer("If you want to get an personalized music suggestion\n"
                         "<b>Describe your feelings with only 1 message and enjoy your music</b>",
                         parse_mode='HTML')

@router.message(SuggestMusic.text)
async def suggested_music_text(message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(SuggestMusic.confirm)
    await message.answer("Check your text and if everything is fine Confirm text", reply_markup=confirmENKb)


@router.message(SuggestMusic.confirm)
async def suggested_music_confirmation(message: Message, state: FSMContext):
    if message.text == "✅Confirm✅":
        # 1. Получаем данные сразу здесь
        data = await state.get_data()
        user_text = data.get("text")

        # 2. Информируем пользователя
        await message.answer("Analyzing your mood... Please wait 🎧", reply_markup=mainENkb)

        # 3. Вызываем ИИ
        ans = await get_music_recommendation(user_text)

        if ans:
            # Текст с моноширинным шрифтом для копирования (тег <code>)
            response_text = (
                f"<b>AI Selection:</b>\n\n"
                f"The playlist that fits your mood: <code>{ans['name']}</code>\n"
                f"<i>Click the name to copy or use the button below.</i>"
            )

            # Красивая кнопка-ссылка
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🎵 Listen Now", url=ans['url'])]
            ])

            await message.answer(response_text, reply_markup=kb, parse_mode='HTML')
        else:
            await message.answer("Sorry, I couldn't find a playlist. Try again later.")

        # 4. Сбрасываем состояние
        await state.clear()

    else:
        await state.clear()
        await message.answer("Canceled successfully", reply_markup=mainENkb)