from django.db import models

from django.contrib.auth import get_user_model

from apps.product.models import Product

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    order = models.BooleanField(default=False)
    total_price = models.DecimalField(decimal_places=2, max_digits=7, default=0.00)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)