from  aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from Keyboards import *
from FSM import *
from MusicRequestsAPI import *
from MUSIC_PLAYLISTS import *
from bot.Texts.MusicTexts import MUSIC_HANDLER_TEXT
from LanguageUtils import get_text, get_user_details

router = Router()


@router.message(F.text == "🎧 Music")
async def music_menu(message: Message):
    await message.answer(await get_text( await get_user_details(message),"music_menu", MUSIC_HANDLER_TEXT), reply_markup=musicENKb, parse_mode='HTML')




@router.message(F.text == "Get suggested music")
async def suggested_music(message, state: FSMContext):
    await state.set_state(SuggestMusic.text)
    await message.answer(await get_text( await get_user_details(message),"suggest_intro", MUSIC_HANDLER_TEXT),
                         parse_mode='HTML')

@router.message(SuggestMusic.text)
async def suggested_music_text(message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(SuggestMusic.confirm)
    await message.answer(await get_text( await get_user_details(message),"check_text", MUSIC_HANDLER_TEXT), reply_markup=confirmENKb)


@router.message(SuggestMusic.confirm)
async def suggested_music_confirmation(message: Message, state: FSMContext):
    if message.text == "✅Confirm✅":
        data = await state.get_data()
        user_text = data.get("text")

        await message.answer(await get_text( await get_user_details(message),"analyzing", MUSIC_HANDLER_TEXT), reply_markup=mainENkb)

        ans = await get_music_recommendation(user_text)

        if ans:
            template = await get_text(await get_user_details(message), "ai_selection", MUSIC_HANDLER_TEXT)

            response_text = template.format(name=ans['name'])


            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=await get_text( await get_user_details(message),"listen_btn", MUSIC_HANDLER_TEXT), url=ans['url'])]
            ])

            await message.answer(response_text, reply_markup=kb, parse_mode='HTML')
        else:
            await message.answer(await get_text( await get_user_details(message),"error_find", MUSIC_HANDLER_TEXT))

        await state.clear()

    else:
        await state.clear()
        await message.answer(await get_text( await get_user_details(message),"canceled", MUSIC_HANDLER_TEXT), reply_markup=mainENkb)



@router.message(F.text == "Playlists")
async def playlists_btn_ans(message: Message):
    text = await get_text( await get_user_details(message),"playlist_header", MUSIC_HANDLER_TEXT)

    for name, url in PLAYLIST_DATA.items():
        text += f"<code>{name}</code>  |  <i><a href='{url}'>Youtube Music</a></i>\n"

    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True, reply_markup=mainENkb)
