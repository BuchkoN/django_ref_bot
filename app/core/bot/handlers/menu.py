from aiogram import (
    F,
    Router,
)
from aiogram.types import Message
from app.core.bot.keyboards.start import InlineFunnelNavigationKeyboard
from app.core.bot.messages.messages import (
    MainMenuButtonsName,
    UserFunnelText,
)
from django.utils.translation import (
    gettext as _,
    gettext_lazy,
)


router = Router()


@router.message(F.text == gettext_lazy(MainMenuButtonsName.SHOW_PROMO))
async def menu_show_promo(message: Message):
    await message.answer(
        text=_(UserFunnelText.first.label),
        reply_markup=InlineFunnelNavigationKeyboard(
            funnel_stage=UserFunnelText.first.name
        ).get_keyboard()
    )
