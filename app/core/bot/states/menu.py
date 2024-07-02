from aiogram.fsm.state import (
    State,
    StatesGroup,
)


class LanguageSelectionFSM(StatesGroup):
    choosing = State()
