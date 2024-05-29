from aiogram.types import InlineKeyboardButton
from app.core.accounts.models import UserLanguageChoices
from app.core.bot.keyboards.base import BaseInlineKeyboard
from django.utils.translation import gettext as _


class InlineLanguageSelectKeyboard(BaseInlineKeyboard):
    def buttons_builder(self):
        return [
            [InlineKeyboardButton(text=_(lang), callback_data=f'select_lang_{value}')]
            for value, lang in UserLanguageChoices.choices
        ]
