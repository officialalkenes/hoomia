from rest_framework import serializers

from apps.product.models import (ProductAttributeValue, ProductCategory, ProductStore,
                                 Product, ProductImage, ProductType, ProductAttribute)

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
