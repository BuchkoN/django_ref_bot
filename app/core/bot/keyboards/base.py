from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import List

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


@dataclass
class BaseInlineKeyboard(ABC):
    @abstractmethod
    def buttons_builder(self) -> List[List[InlineKeyboardButton]]:
        ...

    def get_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=self.buttons_builder())


@dataclass
class BaseReplyKeyboard(ABC):
    @abstractmethod
    def buttons_builder(self) -> List[List[KeyboardButton]]:
        ...

    def get_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(keyboard=self.buttons_builder(), resize_keyboard=True)
