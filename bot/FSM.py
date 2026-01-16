from aiogram.fsm.state import StatesGroup, State


class SuggestMusic(StatesGroup):
    text = State()
    confirm = State()
    receive = State()

class GetPersonalPlan(StatesGroup):
    muscle_group = State()
    duration = State()
    feelings = State()
    confirm = State()
    receive = State()


class Register(StatesGroup):
    weight = State()
    height = State()
    age = State()
    experience = State()
    injuries = State() # Skippable
    description = State()
    save_data = State()

class EditProfile(StatesGroup):
    waiting_for_value = State()