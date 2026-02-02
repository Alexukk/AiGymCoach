INLINE_KB = {
    "edit_profile" : {
        "en" : {"Weight": "weight",
                "Height": "height",
                "Age": "age",
                "Experience": "experience",
                "Injuries": "injuries",
                "Description": "description",
                "Language": "language",},


        "uk" : {"Вага": "weight",
                "Зріст": "height",
                "Вік": "age",
                "Досвід": "experience",
                "Травми": "injuries",
                "Опис": "description",
                "Мова": "language",},
        "UTILS": {
            "en" : "Edit",
            "uk" : ""
        },
        "PREFIX" : "change_"
    },
    "muscle_group" : {
            "en" : {
                "Chest": "1",
                "Back": "2",
                "Legs": "3",
                "Arms + shoulders": "4",
                "Chest + triceps": "5",
                "Back + Biceps": "6",
                "Full body": "7"
            },
            "uk" : {
                "Груди": "1",
                "Спина": "2",
                "Ноги": "3",
                "Руки + плечі": "4",
                "Груди + трицепс": "5",
                "Спина + біцепс": "6",
                "Весь корпус": "7"
            },
            "UTILS": {
                "en": "",
                "uk": ""
            },
        "PREFIX" : "training:"
        }
}



def get_TRAININGS(language):
    if language == "ru":
        language = "uk"
    if language not in ["uk", "en"]:
        language = "en"
    return INLINE_KB["muscle_group"][language]




REPLY_KB = {
    "Confirm" : {
    "en" : ["✅Confirm✅", "❌Cancel❌"],
    "uk" : ["✅Підтвердити✅", "❌Відхилити❌"]
    },
    "MainMenu" : {
        "en" : ["🏋️‍♀️ Trainings", "🎧 Music", "ℹ️ Info", "👤 My Profile"],
        "uk" : ["🏋️‍♀️ Тренування", "🎧 Музика", "ℹ️ Інформація", "👤 Мій профіль"]
    }
}