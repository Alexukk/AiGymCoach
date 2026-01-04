import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from MUSIC_PLAYLISTS import PLAYLIST_DATA, PLAYLIST_NAMES

load_dotenv()
client = genai.Client(api_key=os.getenv("AI_TOKEN"))

SYSTEM_PROMPT = f"""
You are a music expert for a fitness app. Your task is to match the user's workout and emotional state with the perfect playlist.

AVAILABLE PLAYLISTS:
{', '.join(PLAYLIST_NAMES)}

SELECTION RULES:
1. If the user is angry, intense, or doing heavy lifts -> Choose 'Aggressive' or 'Hardcore' versions.
2. If the user is tired, emotional, or doing stretching -> Choose 'Chill' or 'Sad' versions.
3. Return ONLY the exact name of the playlist. No extra text.
"""

PLAYLIST_DATA = {
    "Aggressive Phonk": "https://open.spotify.com/playlist/aggressive_phonk_link",
    "Chill Phonk": "https://open.spotify.com/playlist/chill_phonk_link",
    "Aggressive Metal": "https://open.spotify.com/playlist/aggressive_metal_link",
    "Sad Metal": "https://open.spotify.com/playlist/sad_metal_link",
    "High-Energy Pop": "https://open.spotify.com/playlist/high_energy_pop_link",
    "Deep Techno": "https://open.spotify.com/playlist/deep_techno_link",
    "Hardcore Phonk": "https://open.spotify.com/playlist/hardcore_phonk_link"
}

PLAYLIST_NAMES = list(PLAYLIST_DATA.keys())

async def get_music_recommendation(user_text):

    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",  # Актуальная модель 2026 года
            contents=f"User mood: {user_text}. Pick one from: {', '.join(PLAYLIST_NAMES)}",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a music selector. Return ONLY the exact name from the list provided. "
                    "No extra words, no dots."
                ),
                temperature=0.0,
            )
        )

        name = response.text.strip()

        # Поиск совпадения (даже если ИИ добавил кавычки)
        for key in PLAYLIST_DATA:
            if key.lower() in name.lower():
                return {"name": key, "url": PLAYLIST_DATA[key]}

        # Если не нашли — отдаем дефолт, а не ошибку
        return {"name": "Deep Techno", "url": PLAYLIST_DATA["Deep Techno"]}

    except Exception as e:
        print(f"AI Error: {e}")
        return None