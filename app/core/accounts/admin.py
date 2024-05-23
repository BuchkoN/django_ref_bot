from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from app.core.accounts.models import User
from app.project.settings import USER_MODEL_BASE_REGISTER_FIELD


@admin.register(User)
class UserAdmin(UserAdmin):
    readonly_fields = (
        "date_joined",
        "referral_link",
        "telegram_id",
        "wallet_address",
        "password",
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    USER_MODEL_BASE_REGISTER_FIELD,
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
                )
            },
        ),
        (
            _("Profile"),
            {
                "classes": ("collapse",),
                "fields": (
                    "status",
                    "telegram_id",
                    "referral_link",
                    "wallet_address",
                ),
            },
        ),
    )
    list_filter = ()
    list_display = (
        "id",
        "telegram_id",
        "username",
    )
    search_fields = ("=id", "=telegram_id", "username")
    search_help_text = _("Search by ID, Telegram ID and username")
    ordering = ("-date_joined",)
