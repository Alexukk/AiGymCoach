from Database.requests import get_user_language
from KeyboardsDICTS import INLINE_KB
from bot.Keyboards import Inline_Builder


async def get_text(user_details, text_details, all_texts):
    id, user_lang = user_details
    lang_from_db = await get_user_language(id)
    final_lang = lang_from_db if lang_from_db else user_lang

    if final_lang == "ru":
        final_lang = "uk"

    if final_lang not in ["en", "uk"]:
        final_lang = "en"

    target_dict = all_texts.get(text_details, {})
    return target_dict.get(final_lang, target_dict.get("en", "Error: Text not found"))


async def get_user_details(message):
    return [message.from_user.id,  message.from_user.language_code]



async def get_keyboard(kb_name: str, language: str):
    if kb_name in INLINE_KB.keys():
        base_dict = INLINE_KB[kb_name]
        Utils = base_dict["UTILS"]
        return await Inline_Builder(base_dict[language], Utils[language])
    else:
        return 0


