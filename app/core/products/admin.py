from app.core.products.models import (
    Product,
    ProductRatio,
)
from app.core.referrals.models import ReferralLevelChoices
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class ProductRatioInlineAdmin(admin.TabularInline):
    model = ProductRatio
    can_delete = False
    max_num = ReferralLevelChoices.count_levels()
    min_num = ReferralLevelChoices.count_levels()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prefetch_fields = ('ratios',)

    inlines = (ProductRatioInlineAdmin,)
    list_display = ('id', 'title_ru', 'price')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    ('title_ru', 'title_en'),
                    'price',
                    'deleted_at'
                )
            }
        ),
        (
            _('Description'),
            {
                'classes': ('collapse',),
                'fields': (
                    'description_ru',
                    'description_en',
                )
            }
        )
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(*self.prefetch_fields)
