from rest_framework.serializers import ModelSerializer


from .models import Cart, CartItems


class CartSerializer(ModelSerializer):
    """

    """
    class Meta:
        model = Cart
        exclude = ('user')

    def save():
        pass


class CartItemSerializer(ModelSerializer):
    pass
