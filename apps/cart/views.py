from django.shortcuts import render

from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     UpdateAPIView,
                                    )

from .models import CartItem, Cart
from .serializers import CartSerializer, CartItemSerializer

# Create your views here.
def add_items_to_cart(request):
    serializer = CartSerializer()
    if request.data == 'POST':
        pass


def update_cart_items(request):
    serializer = CartSerializer(data=serializer.data)


