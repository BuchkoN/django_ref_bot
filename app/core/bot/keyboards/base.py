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
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from app.core.bot.messages.messages import MainMenuButtonsName
from django.utils.translation import gettext as _


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


@dataclass
class BaseSubMenyReplyKeyboard(BaseReplyKeyboard):
    with_back: bool = field(default=True, kw_only=True)

    @abstractmethod
    def buttons_builder(self) -> List[List[KeyboardButton]]:
        ...

    def get_keyboard(self) -> ReplyKeyboardMarkup:
        buttons = self.buttons_builder()
        if self.with_back:
            buttons.append([KeyboardButton(text=_(MainMenuButtonsName.MAIN_MENU))])
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
