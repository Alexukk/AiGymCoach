import os
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

STRUCTURE_LEXICON = {
    "uk": {
        "warmup": "Розминка",
        "main": "Основна частина",
        "advice": "Порада тренера",
        "workout_name": "План тренування",
        "rest_label": "Відпочинок",
        "error": "Помилка: Сервіс ШІ тимчасово недоступний."
    },
    "en": {
        "warmup": "Warm-up",
        "main": "Main Work",
        "advice": "Coach's Advice",
        "workout_name": "Workout Plan",
        "rest_label": "Rest",
        "error": "Error: AI service is temporarily unavailable."
    }
}


async def Get_Training_plan(user_text, group, duration, user_profile, language):

    lex = STRUCTURE_LEXICON.get(language, STRUCTURE_LEXICON["en"])
    dynamic_system_prompt = f"""
You are an AI Fitness Coach. 
STRICT RULE: YOU MUST ANSWER EXCLUSIVELY IN THE {language.upper()} LANGUAGE. 
ALL EXERCISE NAMES, HEADERS, AND DESCRIPTIONS MUST BE IN {language.upper()}.

FORMATTING RULES:
1. ONLY USE HTML: <b>, <i>, <u>, <code>. 
2. NO NESTING tags.
3. EMOJIS MUST BE OUTSIDE tags.
4. START DIRECTLY with the workout plan. NO CONVERSATION.

STRUCTURE (COPY THIS FORMAT):
<b>[{lex['workout_name']}]</b>
🎾 <u>{lex['warmup']}</u> (2-3 exercises)
🔥 <u>{lex['main']}</u> (Adjusted for {duration} min)
<b>[Exercise Name in {language}]</b> — <code>Sets x Reps</code> ({lex['rest_label']}: <code>Time</code>)
🧠 <i>{lex['advice']}: [One sentence in {language}]</i>
"""

    try:
        user_prompt = (
            f"TARGET GROUP: {group}\n"
            f"DURATION: {duration} minutes\n"
            f"USER PROFILE: {user_profile}\n"
            f"USER FEELINGS: {user_text}\n"
            f"REPLY ONLY IN: {language}"
        )

        chat_completion = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": dynamic_system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=1500
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Groq API Error: {e}")
        return f"<b>{lex['error']}</b>"