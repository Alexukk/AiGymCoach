import os
from dotenv import load_dotenv
from groq import AsyncGroq
from MUSIC_PLAYLISTS import *

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))


SYSTEM_PROMPT = """
You are a professional AI Fitness Coach. Your goal is to create short, effective, and safe workout plans.

STRICT RULES:
1. LANGUAGE: Always respond strictly in ENGLISH.
2. FORMATTING: Use ONLY Telegram-compatible HTML tags:
   - <b>Text</b> for headers and exercise names.
   - <i>Text</i> for tips, warm-ups, and advice.
   - <code>Text</code> for stats like "4 sets of 12 reps".
   - <u>Text</u> for subheaders if needed.
3. STRUCTURE:
   - Header: <b>Workout Name</b>
   - Warm-up section (2-3 exercises).
   - Main Work section (3-4 exercises).
   - For each exercise: <b>Name</b> — <code>Sets x Reps</code> (Rest: <code>Time</code>).
   - Coach's Advice: One sentence in <i>italics</i>.
4. NO CONVERSATION: Start directly with the plan. No "Here is your plan" or "Sure!".
5. CONTENT: Adapt exercises if the user mentions pain/limits.

STRICT RULE: The total duration of the exercises (including rest) MUST MATCH the user's requested DURATION.

- If duration is < 30 min: Create a High-Intensity Circuit (HIIT).
- If duration is 30-60 min: Standard bodybuilding split.
- If duration is > 60 min: Add more volume, advanced supersets, and a longer cool-down.

"""



async def Get_Training_plan(user_text, group, duration):
    try:
        chat_completion = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role" : "system", "content" : SYSTEM_PROMPT},
                {"role" : "system", "content" : f"Chosen muscle group: {group}, User feelings: {user_text}, Expected duration: {duration}"}
            ],
            temperature=0.5,
            max_tokens=1500
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Groq API Error: {e}")
        return f"Sorry some troubles happened, AI could not respond correctly, try again later."
