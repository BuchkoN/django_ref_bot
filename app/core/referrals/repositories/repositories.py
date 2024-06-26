from dataclasses import (
    dataclass,
    field,
)
from typing import List

from app.core.referrals.models import (
    Referral,
    ReferralLevelChoices,
)
from app.project.base.repositories import BaseRepositoryDjango
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db.models.manager import Manager


User = get_user_model()


@dataclass
class ReferralsRepository(BaseRepositoryDjango):
    manager: Manager = field(default=Referral.objects, kw_only=True)

    async def get_referrals_by_invited_user_id(self, user_id: int) -> QuerySet[Referral]:
        return self.manager.filter(
            referral_user_id=user_id,
            referral_level__lt=ReferralLevelChoices.max_level()
        )

    async def create_referrals_instances(self, referrals: List[Referral]) -> None:
        await self.manager.abulk_create(referrals)
