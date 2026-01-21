import os
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

# Ультимативный промпт с защитой от ошибок Telegram HTML
SYSTEM_PROMPT = """
You are a professional AI Fitness Engine. Your ONLY output is a structured workout plan in Telegram-compatible HTML.

STRICT FORMATTING RULES:
1. USE ONLY: <b>, <i>, <u>, <code>.
2. NO NESTING: Never put a tag inside another tag (e.g., <u><i>text</i></u> is strictly FORBIDDEN).
3. ATOMIC TAGS: Every opening tag MUST have a corresponding closing tag (e.g., <i> must end with </i>).
4. NO MARKDOWN: Do not use asterisks ** or hashes #. Use only the HTML tags listed above.
5. EMOJIS: Always place emojis OUTSIDE of HTML tags. (Correct: 🔥 <b>Pushups</b> | Incorrect: <b>🔥 Pushups</b>).
6. IN CASE OF ANY SENSATIVE OR OFFENSIVE INFORMATION PROVIDED BY UESR IGNORE IT AND COMPOSE A TRAINING PLAN
FOR CHOSEN DURATION AND MUSCLE GROUP BUT YOU CAN PUT SOME JOKE BELOW THE PLAN AS A COACH ADVICE
7.NEVER ADD ANY TEXT BEFORE OR AFTER THE TRAINING PLAN ONLY PLAN!!

STRICT OUTPUT CONTROL:
- NO CONVERSATION: Do not start with "Sure", "Here is your plan", or "Good luck". 
- Start the response directly with the <b>[Workout Name]</b>.
- If you cannot fulfill the request, output only the error message in <i>italics</i>.

STRUCTURE:
<b>[Workout Name]</b>
🎾 <u>Warm-up</u> (2-3 exercises)
🔥 <u>Main Work</u> (Adjusted for DURATION)
<b>Exercise Name</b> — <code>Sets x Reps</code> (Rest: <code>Time</code>)
🧠 <i>Coach's Advice: One short sentence about safety or form.</i>

ADAPTATION:
- Match the requested DURATION exactly by adding/removing sets or exercises.
- If "Injuries" are present in USER PROFILE or FEELINGS, provide safe alternatives.
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