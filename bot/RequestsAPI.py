import os
from dotenv import load_dotenv
from groq import AsyncGroq
from MUSIC_PLAYLISTS import *


load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))


SYSTEM_PROMPT = f"""
You are a music expert for a fitness app. Match the user's mood with a playlist.
AVAILABLE PLAYLISTS: {', '.join(PLAYLIST_NAMES)}

RULES:
1. Return ONLY the exact name of the playlist from the list.
2. No conversation, no dots, no explanations.
3. If user is intense/angry -> Aggressive/Hardcore.
4. If user is tired/stretching -> Chill/Sad.
"""

async def get_music_recommendation(user_text):
    try:
        chat_completion = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.0,
            max_tokens=50
        )

        name = chat_completion.choices[0].message.content.strip()


        for key in PLAYLIST_DATA:
            if key.lower() in name.lower():
                return {"name": key, "url": PLAYLIST_DATA[key]}


        return {"name": "Chill Phonk", "url": PLAYLIST_DATA["Chill Phonk"]}

    except Exception as e:
        print(f"Groq API Error: {e}")

        return {"name": "Chill Phonk", "url": PLAYLIST_DATA["Chill Phonk"]}