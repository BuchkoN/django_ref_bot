from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)
from typing import List

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


@dataclass
class BaseInlineKeyboard(ABC):
    with_back: bool = field(default=True, kw_only=True)

    @abstractmethod
    def buttons_builder(self) -> List[List[InlineKeyboardButton]]:
        ...

    def get_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=self.buttons_builder())
