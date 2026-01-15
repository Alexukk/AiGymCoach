import os
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

# Ультимативный промпт с защитой от ошибок Telegram HTML
SYSTEM_PROMPT = """
You are a professional AI Fitness Coach. Respond strictly in ENGLISH.

STRICT FORMATTING RULES:
1. Use ONLY these HTML tags: <b>, <i>, <u>, <code>.
2. NEVER nest tags (e.g., DO NOT use <u><i>text</i></u>). Use only one tag per word/sentence.
3. Every tag MUST be closed correctly in the right order.
4. Emojis must be OUTSIDE of HTML tags (e.g., 🔥 <b>Text</b>).
5. NO CONVERSATION. Start directly with the workout plan.

STRUCTURE:
- <b>Workout Name</b>
- 🎾 <u>Warm-up</u> (2-3 exercises).
- 🔥 <u>Main Work</u> (Adjust volume based on DURATION).
- <b>Exercise Name</b> — <code>Sets x Reps</code> (Rest: <code>Time</code>).
- 🧠 <i>Coach's Advice: One sentence here.</i>

ADAPTATION:
- Match the requested DURATION exactly.
- If injuries are present in PROFILE or FEELINGS, modify exercises to be safe.
"""


async def Get_Training_plan(user_text, group, duration, user_profile):
    try:
        # Формируем запрос
        user_prompt = (
            f"TARGET GROUP: {group}\n"
            f"DURATION: {duration} minutes\n"
            f"USER PROFILE: {user_profile}\n"
            f"CURRENT FEELINGS: {user_text}"
        )

        chat_completion = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,  # Чуть ниже для стабильности структуры
            max_tokens=1500
        )

        response = chat_completion.choices[0].message.content
        return response

    except Exception as e:
        print(f"Groq API Error: {e}")
        return "<b>Error:</b> AI service is temporarily unavailable. Please try again."