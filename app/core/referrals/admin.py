from app.core.referrals.models import Referral
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    related_fields = (
        "invited_user",
        "referral_user"
    )
    readonly_fields = (
        "get_invited_username",
        "get_referral_username",
    )
    list_display = (
        "id",
        "get_invited_username",
        "get_referral_username",
        "referral_level",
    )
    fieldsets = (
        (
            None,
            {
                'fields': (
                    ('invited_user', 'referral_user'),
                    'referral_level'
                )
            }
        ),
    )

    @admin.display(description=_('Invited username'))
    def get_invited_username(self, instance: Referral) -> str:
        return instance.invited_user.username

    @admin.display(description=_('Referral username'))
    def get_referral_username(self, instance: Referral) -> str:
        return instance.referral_user.username

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(*self.related_fields)


class ReferralInlineAdmin(admin.TabularInline):
    model = Referral
    fk_name = 'invited_user'
    extra = 0

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'referral_user',
                    'referral_level',
                )
            }
        ),
    )
