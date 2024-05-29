from app.core.referrals.models import (
    Referral,
    ReferralLevelChoices,
)
from django.contrib.auth import get_user_model
from django.db.models import QuerySet


User = get_user_model()


async def get_referrals_chain_by_invited_user(invited_user: User) -> QuerySet[Referral]:
    return invited_user.invited.filter(
        referral_level__lt=ReferralLevelChoices.max_level()
    )
