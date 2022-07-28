from email.policy import default
from django.db import models

from django.utils.translation import gettext_lazy as _

from apps.common.models import AbstractModel

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

class ProductCategory(MPTTModel):
    """
    Product Category like clothes, bags and other key accessories
    """
    name = models.CharField(max_length=100, verbose_name=_("Category Name"),
                                )
    slug = models.SlugField(max_length=100, blank=True,
                            verbose_name=_("Category Slug"))

    parent = TreeForeignKey('self', on_delete=models.PROTECT,
                            related_name='children',
                            null=True, blank=True,
                            verbose_name= _("Category Parent"),
                            help_text = _("format: Not required"))

    def __str__(self) -> str:
        return f'{self.category}'

    class MPTTMeta:
        order_by_insertion = ['name']

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")


class Product(AbstractModel):
    """
    Product Table
    """
    name = models.CharField(max_length=120, verbose_name=_("Product Name"), 
                            unique=True)
    slug = models.SlugField(max_length=120, verbose_name=_("Product Slug"))
    category = TreeManyToManyField(ProductCategory,
                                 related_name='product-cat')
    description = models.TextField(verbose_name=_("Product Description"))
    confirmed = models.BooleanField(default=False, verbose_name="Product Availability",
                                    help_text=_("format: bool, true=product available"))

    # price = models.DecimalField(max_digits=8, decimal_places=2,
    #                             verbose_name=_("Product Price"))
    # discount = models.DecimalField(max_digits=3, decimal_places=3)
    # image = models.ImageField()


class ProductType(models.Model):
    pass


class ProductAttributeValue(models.Model):
    pass

class Brand(models.Model):
    pass


class ProductStore(AbstractModel):
    """
    Product Inventory/Store
    """
    sku = models.CharField(max_length=30, verbose_name=_("stock keeping unit"),
                           unique=True, help_text=_("format: required, unique = True, max-30"),
                           blank=True)
    pc = models.CharField(max_length=30, verbose_name=_("product code"),
                           unique=True, help_text=_("format: required, unique = True, max-30"),
                           blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT,
                                     related_name='product_type', verbose_name=_("Product Type"))
    product = models.ForeignKey(Product,  on_delete=models.PROTECT,
                                     related_name='product_type', verbose_name=_("Product Type"))
    brand = models.ForeignKey(Brand,  on_delete=models.PROTECT,
                                     related_name='product_type', verbose_name=_("Product Type"))
    attribute_val = models.ManyToManyField(ProductAttributeValue, related_name='product_attr_val')
    confirmed = models.BooleanField(default=False, verbose_name="Product Availability",
                                    help_text=_("format: bool, true=product available"))
    retail_price = models.DecimalField(max_digits=6, verbose_name=_("Product Retail Price"),
                                       decimal_places=2, help_text=_("format: required, value: 0.2f"),
                                       error_messages={
                                           'price': {
                                               'max_digits': _("Price must not exceed 9999.99")
                                           },
                                       },
                                       )

    store_price = models.DecimalField(max_digits=6, verbose_name=_("Product Store Price"),
                                       decimal_places=2, help_text=_("format: required, value: 0.2f"),
                                       error_messages={
                                           'price': {
                                               'max_digits': _("Price must not exceed 9999.99")
                                           },
                                       },
                                       )
    sale_price = models.DecimalField(max_digits=6, verbose_name=_("Product Sale Price"),
                                        decimal_places=2, help_text=_("format: required, value: 0.2f"),
                                        error_messages={
                                            'price': {
                                                'max_digits': _("Price must not exceed 9999.99")
                                            },
                                        },
                                        )
