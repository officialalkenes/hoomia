from django.db import models

from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

from apps.product.models import Product

User = get_user_model()


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.BooleanField(default=False)
    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    cart_item = models.ManyToManyField(CartItem)
    order = models.BooleanField(default=False)
    total_price = models.DecimalField(decimal_places=2, max_digits=7, default=0.00)

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    @property
    def total_cart_price(self):
        price = [0 + x.product__price for x in self.cart_item]
        return price
    