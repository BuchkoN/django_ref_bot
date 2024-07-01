from aiogram import (
    F,
    Router,
)
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
from app.core.bot.keyboards.user import (
    InlineFunnelNavigationKeyboard,
    InlineLanguageSelectKeyboard,
)
from app.core.bot.messages.messages import (
    BotMessagesText,
    UserFunnelText,
)
from app.core.bot.utils import extract_ref_code
from app.core.referrals.services.services import ReferralService
from django.contrib.auth import get_user_model
from django.utils import translation
from django.utils.translation import gettext as _


router = Router()
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
        text=_(BotMessagesText.SELECT_LANG),
        reply_markup=InlineLanguageSelectKeyboard(with_back=False).get_keyboard()
    )


@router.callback_query(F.data.startswith('select_lang'))
async def user_select_language(call: CallbackQuery):
    language = call.data.split('_')[-1]
    await UsersRepository().change_language_for_telegram_user(
        user_tg_id=call.from_user.id,
        language=language
    )
    with translation.override(language=language):
        await call.message.edit_text(
            text=_(UserFunnelText.first.label),
            reply_markup=InlineFunnelNavigationKeyboard(
                funnel_stage=UserFunnelText.first.name
            ).get_keyboard()
        )


@router.callback_query(F.data.startswith('funnel'))
async def user_funnel(call: CallbackQuery):
    funnel_stage = call.data.split('_')[-1]
    user_repo = UsersRepository()
    if funnel_stage == UserFunnelText.fifth.name:
        await user_repo.telegram_user_completed_funnel(call.from_user.id)
        await call.message.edit_text(_("Funnel is completely"))
        return

    await call.message.edit_text(
        text=_(getattr(UserFunnelText, funnel_stage).label),
        reply_markup=InlineFunnelNavigationKeyboard(funnel_stage=funnel_stage).get_keyboard()
    )
