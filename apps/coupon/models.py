import os
import datetime

from django.contrib.auth import get_user_model

from django.db import models

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_("coupon"))
    coupon_tag = models.CharField(max_length=50, verbose_name=_("Coupon Tag"))
    coupon_code = models.CharField(max_length=8, verbose_name=_("Coupon Code"))
    discount = models.DecimalField(decimal_places=2, max_digits=3, default=0.00,
                                   help_text=_('format: 0.05 == 5%, 0.2 == 20%'))
    amount_discounted = models.DecimalField(max_digits=7, verbose_name=_('Discounted Ammount'),
                                            decimal_places=2)
    minimum_purchase = models.DecimalField(max_digits=6, default=100.00, decimal_places=2)
    expired = models.BooleanField(default=False, verbose_name=_("Expiry Boolean"))
    from_date = models.DateField(blank=True, verbose_name=_("Coupon Started"))
    to_date = models.DateField(blank=True, verbose_name=_("Coupon Ended"))

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __str__(self) -> str:
        return f'{self.user.username} - {self.coupon_code}'

    def save(self, *args, **kwargs):
        today = datetime.today()
        if self.from_date <= today and self.to_date >= today:
            self.expired = False
        self.expired = True

        return super().save(self, *args, **kwargs)