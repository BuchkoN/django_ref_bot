from app.core.accounts.repositories.repositories import get_user_by_telegram_id
from app.core.referrals.models import (
    Referral,
    ReferralLevelChoices,
)
from app.core.referrals.repositories.repositories import get_referrals_chain_by_invited_user
from django.contrib.auth import get_user_model


User = get_user_model()


async def create_referrals_instances(invited_user_id: int, referral: User) -> None:
    invited_user: User = await get_user_by_telegram_id(telegram_id=invited_user_id)
    if invited_user is None:
        return

    referrals_create = [Referral(
        invited_user_id=invited_user.id,
        referral_user_id=referral.id,
        referral_level=ReferralLevelChoices.first
    )]

    referrals_chain = await get_referrals_chain_by_invited_user(invited_user)
    async for ref_instance in referrals_chain:
        referrals_create.append(Referral(
            invited_user_id=ref_instance.invited_user_id,
            referral_user_id=referral.id,
            referral_level=ref_instance.referral_level + 1,
        ))

    await Referral.objects.abulk_create(referrals_create)
