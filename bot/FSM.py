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
