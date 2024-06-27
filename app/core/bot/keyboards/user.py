from dataclasses import (
    dataclass,
    field,
)

from aiogram.types import InlineKeyboardButton
from app.core.accounts.models import UserLanguageChoices
from app.core.bot.keyboards.base import BaseInlineKeyboard
from app.core.bot.messages.messages import UserFunnelText
from django.utils.translation import gettext as _


@dataclass
class InlineLanguageSelectKeyboard(BaseInlineKeyboard):
    with_back: bool = field(default=True, kw_only=True)

    def buttons_builder(self):
        return [
            [InlineKeyboardButton(text=_(lang), callback_data=f'select_lang_{value}')]
            for value, lang in UserLanguageChoices.choices
        ]


@dataclass
class InlineFunnelNavigationKeyboard(BaseInlineKeyboard):
    funnel_stage: str

    def buttons_builder(self):
        keyboard = [[
            InlineKeyboardButton(
                text=_('Next'),
                callback_data=f'funnel_{UserFunnelText.get_next_funnel_label(self.funnel_stage)}')
        ]]
        if self.funnel_stage != UserFunnelText.first.name:
            keyboard.append([InlineKeyboardButton(
                text=_('Back'),
                callback_data=f'funnel_{UserFunnelText.get_prev_funnel_label(self.funnel_stage)}'
            )])
        return keyboard
