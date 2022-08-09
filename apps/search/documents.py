from django.conf import settings
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from apps.product.models import ProductStore, Product, ProductCategory



@registry.register_document
class ProductInventoryDocument(Document):
    product = fields.ObjectField(
        properties = {
            'name': fields.TextField()
        }
    )

    class Index:
        name = 'productinventory'
        settings = {'number_of_shards' : 1,
                    'number_of_replicas': 0
                    }
    class Django:
        model = ProductStore
        fields = [
            'id',
            'price',
        ]
        