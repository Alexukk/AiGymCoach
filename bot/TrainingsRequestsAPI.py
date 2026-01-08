import os
from dotenv import load_dotenv
from groq import AsyncGroq
from MUSIC_PLAYLISTS import *

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))


SYSTEM_PROMPT = """ FOR NOW JUST RETURN SOME TRAINING PLAN TO TEST 
                
"""


async def Get_Training_plan(user_text, group):
    try:
        chat_completion = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role" : "system", "content" : SYSTEM_PROMPT},
                {"role" : "system", "content" : f"Chosen muscle group: {group}, User feelings: {user_text}"}
            ],
            temperature=0.0,
            max_tokens=800
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Groq API Error: {e}")
        return f"Sorry some troubles happened, AI could not respond correctly, try again later."
