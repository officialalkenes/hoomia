from django.db import models

from django.contrib.auth import get_user_model

from apps.product.models import Product

from django.utils.translation import gettext_lazy as _

User = get_user_model()


class ItemOrder(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE,
                                   related_name=_('order'))
    is_ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name=_("order_owner"))
    item_ordered = models.ManyToManyField(ItemOrder, verbose_name=_("Ordered Item"))
    ordered = models.BooleanField(default=False,
                                  help_text=_("format: bool, Boolean Check to seperate confirmed order from new"))
    creation_date = models.DateTimeField(auto_now_add=True)

