from requests import Response
from rest_framework import  decorators, permissions, response, status, viewsets

from .serializers import ProductCategorySerializer, ProductSerializer

from apps.product.models import (Product, ProductAttribute, ProductAttributeValue,
                                 ProductCategory, ProductImage, ProductStore, ProductType)

class AllProductCategory(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductCategorySerializer()

@decorators.api_view(['GET'])
def all_category_list_view(request):
    if request.method == 'GET':
        product_cat = ProductCategory.objects.all()
        serializer = ProductCategory(product_cat, many=True)
        return response.Response(serializer.data)

@decorators.api_view(['GET', 'PUT'])
def category_detail(request, pk):
    try:
        category = ProductCategory.objects.get(id=pk)
    except ProductCategory.DoesNotExist:
        return response.Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductCategorySerializer(category)
        return response.Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductCategorySerializer(category, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(['DELETE'])
def category_modify_view(request, pk):
    """
        Restricted Permissions => only Admins.. Other permission can be Implemented
    """
    try:
        category = ProductCategory.objects.get(id=pk)
    except ProductCategory.DoesNotExist:
        return response.Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        category.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ProductApiView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = permissions.IsAuthenticatedOrReadOnly()
    serializer_class = ProductSerializer()
    lookup_field = 'slug'
