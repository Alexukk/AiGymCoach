from Database.requests import get_user_language

async def get_text(tg_id, text_details, user_lang, all_texts):
    lang_from_db = await get_user_language(tg_id)
    final_lang = lang_from_db if lang_from_db else user_lang

    if final_lang == "ru":
        final_lang = "uk"

    if final_lang not in ["en", "uk"]:
        final_lang = "en"

    target_dict = all_texts.get(text_details, {})
    return target_dict.get(final_lang, target_dict.get(final_lang, "Error: Text not found"))

