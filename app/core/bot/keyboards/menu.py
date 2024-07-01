from dataclasses import (
    dataclass,
    field,
)

from aiogram.types import KeyboardButton
from app.core.bot.keyboards.base import BaseReplyKeyboard
from app.core.bot.messages.messages import MainMenuButtonsName
from django.utils.translation import gettext as _


@dataclass
class ReplyMainMenuKeyboard(BaseReplyKeyboard):
    full_menu: bool = field(default=False)

    @staticmethod
    def _base_menu_buttons():
        return [
            [KeyboardButton(text=_(MainMenuButtonsName.SETTINGS))],
            [KeyboardButton(text=_(MainMenuButtonsName.SHOW_PROMO))],
        ]

    @staticmethod
    def _full_menu_buttons():
        return [
            [KeyboardButton(text=_(MainMenuButtonsName.SETTINGS))],
        ]

    def buttons_builder(self):
        if not self.full_menu:
            return self._base_menu_buttons()
        return self._full_menu_buttons()
