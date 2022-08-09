import numpy as np

from django.contrib.auth import get_user_model

from django.db import models

from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from apps.common.models import BaseModel
from apps.product.models import Product

User = get_user_model()

class ProductReview(models.Model):
    class StarRating(models.IntegerChoices):
        poor = (1, 1)
        fair = (2, 2)
        good = (3, 3)
        better = (4, 4)
        excellent = (4, 4)

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='review')
    product = models.ForeignKey(Product, related_name=_("purchased_product"),
                                on_delete=models.SET_NULL)
    comment = models.TextField(blank=True)
    ratings = models.IntegerField(choices=StarRating)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.product.name}'

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

