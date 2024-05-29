from aiogram import F
from aiogram.filters import (
    Command,
    CommandObject,
    CommandStart,
)
from aiogram.types import (
    CallbackQuery,
    Message,
)
from app.core.accounts.repositories.repositories import (
    get_or_create_user_from_telegram,
    get_user_by_telegram_id,
)
from app.core.bot.handlers.base import LocalizedRouter
from app.core.bot.keyboards.user import InlineLanguageSelectKeyboard
from app.core.referrals.services.services import create_referrals_instances
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


router = LocalizedRouter()
User = get_user_model()


@router.message(Command('start'))
@router.message(CommandStart(deep_link=True))
async def user_start(message: Message, command: CommandObject):
    user, is_created = await get_or_create_user_from_telegram(message.chat)
    if command.args is not None and command.args.isdigit() and is_created:
        await create_referrals_instances(int(command.args), user)
    await message.answer(
        text=_('Please select a language'),
        reply_markup=InlineLanguageSelectKeyboard(with_back=False).get_keyboard()
    )


@router.callback_query(F.data.startswith('select_lang'))
async def user_select_language(call: CallbackQuery):
    user: User = await get_user_by_telegram_id(telegram_id=call.from_user.id)
    await User.objects.filter(id=user.id).aupdate(language=call.data.split('_')[-1])
    await call.message.delete()
