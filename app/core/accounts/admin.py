from app.core.accounts.models import User
from app.core.referrals.admin import ReferralInlineAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(UserAdmin):
    readonly_fields = (
        "date_joined",
        "telegram_username",
        "telegram_id",
        "wallet_address",
        "oid",
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    User.USERNAME_FIELD,
                    "password1",
                    "password2",
                    "is_staff",
                ),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "password",
                    "language",
                    "last_login",
                    "date_joined",
                    "is_staff",
                    "oid",
                )
            },
        ),
        (
            _("Profile"),
            {
                "classes": ("collapse",),
                "fields": (
                    "status",
                    'telegram_username',
                    "telegram_id",
                    "wallet_address",
                ),
            },
        ),
    )
    list_filter = ()
    list_display = (
        "id",
        User.USERNAME_FIELD,
        "telegram_username",
        "telegram_id",
    )
    prefetch_fields = ("referrals",)
    inlines = (ReferralInlineAdmin,)
    search_fields = ("=id", "=telegram_id", "username")
    search_help_text = _("Search by ID, Telegram ID and username")
    ordering = ("-date_joined",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(*self.prefetch_fields)
