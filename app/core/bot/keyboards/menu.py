from dataclasses import (
    dataclass,
    field,
)

from aiogram.types import KeyboardButton
from app.core.accounts.models import UserLanguageChoices
from app.core.bot.keyboards.base import (
    BaseReplyKeyboard,
    BaseSubMenyReplyKeyboard,
)
from app.core.bot.messages.messages import (
    MainMenuButtonsName,
    ReferralMenuButtonsName,
    SettingsMenuButtonsName,
)
from django.utils.translation import gettext as _


class ReferralMenuReplyKeyboard(BaseSubMenyReplyKeyboard):
    def buttons_builder(self):
        return [[KeyboardButton(text=_(ReferralMenuButtonsName.GET_REF_LINK))]]


class ChangeLanguageReplyKeyboard(BaseSubMenyReplyKeyboard):
    def buttons_builder(self):
        return [[KeyboardButton(text=_(lang)) for value, lang in UserLanguageChoices.choices]]


@dataclass
class SettingsMenuReplyKeyboard(BaseSubMenyReplyKeyboard):
    full_menu: bool = field(default=False)

    @staticmethod
    def _base_menu_buttons():
        return [[KeyboardButton(text=_(SettingsMenuButtonsName.CHANGE_LANGUAGE))]]

    @staticmethod
    def _full_menu_buttons():
        return [[KeyboardButton(text=_(SettingsMenuButtonsName.CHANGE_LANGUAGE))]]

    def buttons_builder(self):
        return (
            self._base_menu_buttons() if not self.full_menu
            else self._full_menu_buttons()
        )


@dataclass
class MainMenuReplyKeyboard(BaseReplyKeyboard):
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
            [KeyboardButton(text=_(MainMenuButtonsName.REFERRAL_MENU))]
        ]

    def buttons_builder(self):
        return (
            self._base_menu_buttons() if not self.full_menu
            else self._full_menu_buttons()
        )
