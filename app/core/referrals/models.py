from django.db import models
from django.utils.translation import gettext_lazy as _


class ReferralLevelChoices(models.IntegerChoices):
    """Уровни рефералов"""

    first = 1, _("Level 1")
    second = 2, _("Level 2")
    third = 3, _("Level 3")
    fourth = 4, _("Level 4")
    fifth = 5, _("Level 5")


class Referral(models.Model):
    invited_user = models.ForeignKey(
        'accounts.User',
        verbose_name=_("Invited User"),
        on_delete=models.PROTECT,
        related_name='referrals',
        null=False
    )
    referral_user = models.ForeignKey(
        'accounts.User',
        verbose_name=_("Referral User"),
        on_delete=models.PROTECT,
        related_name='invited',
        null=False
    )
    referral_level = models.PositiveSmallIntegerField(
        _("Referral Level"),
        choices=ReferralLevelChoices.choices,
        null=ReferralLevelChoices.first,
    )

    class Meta:
        verbose_name = _("Referral")
        verbose_name_plural = _("Referrals")
        indexes = [models.Index(fields=["referral_level"])]
        unique_together = [
            ('invited_user', 'referral_user')
        ]

    def __str__(self):
        return _(self._meta.verbose_name) + f' ID {self.id}'
