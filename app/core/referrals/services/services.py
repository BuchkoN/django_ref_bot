from app.core.accounts.repositories.repositories import UsersRepository
from app.core.referrals.models import (
    Referral,
    ReferralLevelChoices,
)
from app.core.referrals.repositories.repositories import ReferralsRepository
from app.project.base.services import BaseService
from django.contrib.auth import get_user_model


User = get_user_model()


class ReferralService(BaseService):
    @staticmethod
    async def add_referrals_by_ref_code(new_user: User, ref_code: str) -> None:
        invited_user = await UsersRepository().get_user_by_oid(oid=ref_code)
        if invited_user is None:
            return

        referrals_repo = ReferralsRepository()
        new_referrals = [Referral(
            invited_user_id=invited_user.id,
            referral_user_id=new_user.id,
            referral_level=ReferralLevelChoices.first
        )]
        async for ref in await referrals_repo.get_referrals_by_invited_user_id(invited_user.id):
            new_referrals.append(Referral(
                invited_user_id=ref.invited_user_id,
                referral_user_id=new_user.id,
                referral_level=ref.referral_level + 1,
            ))
        await referrals_repo.create_referrals_instances(new_referrals)
