from aiogram import (
    F,
    Router,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.core.accounts.models import UserLanguageChoices
from app.core.accounts.repositories.repositories import UsersRepository
from app.core.bot.filters import FunnelPassedUserFilter
from app.core.bot.keyboards.menu import (
    ChangeLanguageReplyKeyboard,
    MainMenuReplyKeyboard,
    ReferralMenuReplyKeyboard,
    SettingsMenuReplyKeyboard,
)
from app.core.bot.keyboards.start import InlineFunnelNavigationKeyboard
from app.core.bot.messages.messages import (
    BotMessagesText,
    MainMenuButtonsName,
    ReferralMenuButtonsName,
    SettingsMenuButtonsName,
    UserFunnelText,
)
from app.core.bot.states.menu import LanguageSelectionFSM
from django.contrib.auth import get_user_model
from django.utils import translation
from django.utils.translation import (
    gettext as _,
    gettext_lazy,
)


router = Router()
User = get_user_model()


@router.message(F.text == gettext_lazy(MainMenuButtonsName.MAIN_MENU))
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    user = await UsersRepository().get_user_by_telegram_id(telegram_id=message.from_user.id)
    await message.answer(
        text=_(BotMessagesText.MAIN_MENU),
        reply_markup=MainMenuReplyKeyboard(full_menu=user.is_funnel_passed).get_keyboard()
    )


@router.message(F.text == gettext_lazy(MainMenuButtonsName.SHOW_PROMO))
async def menu_show_promo(message: Message):
    await message.answer(
        text=_(UserFunnelText.first.label),
        reply_markup=InlineFunnelNavigationKeyboard(
            funnel_stage=UserFunnelText.first.name
        ).get_keyboard()
    )


@router.message(F.text == gettext_lazy(MainMenuButtonsName.SETTINGS))
async def menu_settings(message: Message):
    user = await UsersRepository().get_user_by_telegram_id(telegram_id=message.from_user.id)
    await message.answer(
        text=_(BotMessagesText.SETTINGS_MENU),
        reply_markup=SettingsMenuReplyKeyboard(full_menu=user.is_funnel_passed).get_keyboard()
    )


@router.message(F.text == gettext_lazy(SettingsMenuButtonsName.CHANGE_LANGUAGE))
async def manu_change_language(message: Message, state: FSMContext):
    await message.answer(
        text=_(BotMessagesText.SELECT_LANG),
        reply_markup=ChangeLanguageReplyKeyboard().get_keyboard()
    )
    await state.set_state(LanguageSelectionFSM.choosing)


@router.message(LanguageSelectionFSM.choosing)
async def menu_select_language(message: Message, state: FSMContext):
    user_repo = UsersRepository()
    user = await user_repo.get_user_by_telegram_id(telegram_id=message.from_user.id)
    if message.text not in UserLanguageChoices.labels:
        await message.answer(
            text=_(BotMessagesText.INVALID_LANGUAGE),
            reply_markup=MainMenuReplyKeyboard(full_menu=user.is_funnel_passed).get_keyboard()
        )
        await state.clear()
        return

    language = UserLanguageChoices.names[UserLanguageChoices.labels.index(message.text)]
    await user_repo.change_language_for_telegram_user(
        user_tg_id=user.telegram_id,
        language=language
    )
    with translation.override(language):
        await message.answer(
            text=_(BotMessagesText.SUCCESS_CHANGE_LANGUAGE),
            reply_markup=MainMenuReplyKeyboard(full_menu=user.is_funnel_passed).get_keyboard()
        )
    await state.clear()


@router.message(
    FunnelPassedUserFilter(),
    F.text == gettext_lazy(MainMenuButtonsName.REFERRAL_MENU)
)
async def menu_referral(message: Message, user: User):
    await message.answer(
        text=_(BotMessagesText.REFERRAL_MENU),
        reply_markup=ReferralMenuReplyKeyboard().get_keyboard()
    )


@router.message(
    FunnelPassedUserFilter(),
    F.text == gettext_lazy(ReferralMenuButtonsName.GET_REF_LINK)
)
async def menu_get_referral_link(message: Message, user: User):
    await message.answer(
        text=_(BotMessagesText.REFERRAL_LINK).format(user.referral_link),
        reply_markup=MainMenuReplyKeyboard(full_menu=True).get_keyboard()
    )
