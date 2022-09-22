from django.db import models

from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

from apps.product.models import Product

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    order = models.BooleanField(default=False)
    total_price = models.DecimalField(decimal_places=2, max_digits=7, default=0.00)

    @property
    def get_total_cart_price(self):
        pass

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")