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
async def suggested_music_confirmation(message, state: Message):
    if message.text == "✅Confirm✅":
        await state.set_state(SuggestMusic.receive)
    else:
        await state.clear()
        await message.answer("Canceled successfully", reply_markup=mainENkb)

@router.message(SuggestMusic.receive)
async def suggested_music_ending(message, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    await message.answer("Your request is being processed.", reply_markup=mainENkb)
    await Music_request(text)