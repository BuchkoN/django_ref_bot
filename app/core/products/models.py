from app.core.referrals.models import ReferralLevelChoices
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Product(models.Model):
    title_ru = models.CharField(_("Title RU"), max_length=25)
    title_en = models.CharField(_("Title EN"), max_length=25)
    description_ru = models.TextField(_("Description RU"), max_length=1000)
    description_en = models.TextField(_("Description EN"), max_length=1000)
    price = models.DecimalField(_("Price"), max_digits=15, decimal_places=10, null=False)
    deleted_at = models.DateTimeField(_("Deleted at"), blank=True, null=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return _(self._meta.verbose_name) + f' ID {self.id}'


class ProductRatio(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.PROTECT,
        related_name="ratios",
        null=False
    )
    referral_level = models.PositiveSmallIntegerField(
        _("Referral level"),
        choices=ReferralLevelChoices.choices,
        default=None,
        null=False,
    )
    ratio = models.DecimalField(
        _("Ratio"),
        validators=[MaxValueValidator(1)],
        max_digits=25,
        decimal_places=10,
        null=False
    )

    class Meta:
        verbose_name = _("Product ratio")
        verbose_name_plural = _("Product ratios")
        indexes = [models.Index(fields=["referral_level", "product_id"])]
        unique_together = [
            ('product_id', 'referral_level')
        ]

    def __str__(self):
        return _(self._meta.verbose_name) + f' Product ID {self.product_id}'
