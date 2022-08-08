from rest_framework import serializers

from rest_framework.fields import CurrentUserDefault


from apps.product.models import (Brand, ProductAttributeValue,
                                 ProductCategory, ProductStore,
                                 Product, ProductImage, ProductType,
                                 ProductAttribute)


class VendorProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = '__all__'

    def save(self):
        user = CurrentUserDefault()  # <= magic!



class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['name']


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        exclude = ['id']



class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        exclude = ['pkid', 'id']


class ProductAttributeValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttributeValue
        exclude = ['pkid', 'id']


class ProductSerializer(serializers.ModelSerializer):
    image_path = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ['id', 'pkid']

    def get_image_path(self, obj):
        return self.context['request'].build_absolute_uri(obj.image_path.url)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']
        read_only = True


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['name']
        read_only = True


class ProductInventorySerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False, read_only=True)
    product_attribute = ProductAttributeValueSerializer(
                        source='product_attribute_value',
                        many=True, read_only=True)

    product = ProductSerializer(many=False,
                                read_only=True)

    images = ProductImageSerializer(source='product_image',
                                    many=True)

    product_type = ProductTypeSerializer(many=False)

    class Meta:
        models = ProductStore
        fields = ('sku', 'pc', 'product_type', 'product',
                  'brand', 'attribute_val', 'retail_price',
                  'product_att_val', 'store_price',
                  'sale_price', 'discount_percentage',
                  'weight', 'weight_type')


