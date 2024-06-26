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
from app.core.accounts.repositories.repositories import UsersRepository
from app.core.bot.handlers.base import LocalizedRouter
from app.core.bot.keyboards.user import InlineLanguageSelectKeyboard
from app.core.bot.utils import extract_ref_code
from app.core.referrals.services.services import ReferralService
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


router = LocalizedRouter()
User = get_user_model()


@router.message(Command('start'))
@router.message(CommandStart(deep_link=True))
async def user_start(message: Message, command: CommandObject):
    user_repo = UsersRepository()
    user, is_created = await user_repo.get_or_create_user_from_telegram_chat(message.chat)
    ref_code = extract_ref_code(command.args)
    if ref_code is not None and is_created:
        await ReferralService().add_referrals_by_ref_code(user, ref_code)
    await message.answer(
        text=_('Please select a language'),
        reply_markup=InlineLanguageSelectKeyboard(with_back=False).get_keyboard()
    )


@router.callback_query(F.data.startswith('select_lang'))
async def user_select_language(call: CallbackQuery):
    user_repo = UsersRepository()
    user: User = await user_repo.get_user_by_telegram_id(telegram_id=call.from_user.id)
    await User.objects.filter(id=user.id).aupdate(language=call.data.split('_')[-1])
    await call.message.delete()
