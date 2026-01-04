from aiogram.fsm.state import StatesGroup, State


class SuggestMusic(StatesGroup):
    text = State()
    confirm = State()
    receive = State()


