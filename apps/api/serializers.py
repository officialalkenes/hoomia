from rest_framework import serializers

from apps.product.models import (Brand, ProductAttributeValue, ProductCategory, ProductStore,
                                 Product, ProductImage, ProductType, ProductAttribute)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        exclude = ['']



class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttributeValue
        exclude = ['pkid', 'id']


class ProductAttributeValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttributeValue
        exclude = ['pkid', 'id']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductInventorySerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False, read_only=True)
    product_attribute_value = ProductAttributeValueSerializer(many=True, read_only=True)

    class Meta:
        models = ProductStore
        fields = ('sku', 'pc', 'product_type', 'product', 'brand', 'attribute_val', 'retail_price', 'product_att_val', 'store_price', 'sale_price', 'discount_percentage', 'weight', 'weight_type')

