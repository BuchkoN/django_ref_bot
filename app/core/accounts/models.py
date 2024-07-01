from django.apps import apps
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    PermissionsMixin,
    UserManager as AbstractUserManager,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField


class UserStatusChoices(models.IntegerChoices):
    """Статусная модель пользователя"""

    funnel_not_passed = 1, _("Did not pass the funnel")
    funnel_passed = 2, _("Passed the funnel")
    purchased_free_product = 3, _("Purchased a free product")
    purchased_paid_product = 4, _("Purchased a paid product")


class UserLanguageChoices(models.TextChoices):
    """Язык интерфейса пользователя"""

    russian = "ru", _("Russian")
    english = "en", _("English")


class UserManager(AbstractUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """Создание пользователя по username"""

        if not username:
            raise ValueError("The given username must be set")

        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    oid = ShortUUIDField("OID", editable=False)
    username = models.CharField(_("Username"), max_length=250, blank=True, unique=True)
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True)
    telegram_username = models.CharField(_("Telegram username"), max_length=250, null=True)
    telegram_id = models.BigIntegerField("Telegram ID", blank=True, null=True)
    wallet_address = models.CharField(_("Wallet address"), max_length=250, null=True)
    language = models.CharField(
        _("Interface language"),
        choices=UserLanguageChoices.choices,
        default=UserLanguageChoices.english
    )
    status = models.PositiveSmallIntegerField(
        _("Status"),
        choices=UserStatusChoices.choices,
        default=UserStatusChoices.funnel_not_passed
    )
    is_staff = models.BooleanField(
        _("Staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    objects = UserManager()
    USERNAME_FIELD = settings.USER_MODEL_BASE_REGISTER_FIELD

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]
        indexes = [models.Index(fields=["telegram_id"])]

    @property
    def is_funnel_passed(self) -> bool:
        return self.status != UserStatusChoices.funnel_not_passed
