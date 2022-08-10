from django.db import models

from django.utils.translation import gettext_lazy as _

from django.utils.text import slugify

from apps.common.models import BaseModel

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

from django.contrib.auth import get_user_model

User = get_user_model()

"""
    the hierarchy of the models are not Entirely Ignored.
"""


class ProductCategory(MPTTModel):
    """
    Product Category like clothes, Electronics, Computers
    Child Categories Like Headphones from parent Electronics, Monitors and servers in Computers
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(self, *args, **kwargs)

class Product(BaseModel):
    """
    Product Table
    id -> primary key of the table (hidden)
    pkid -> search reference of the table. unique
    created -> auto-added on save
    updatd -> auto-added on modify
    owner -> vendor's Account
    name -> format(str) e.g Airmax shoe
    slug -> search reference
    category -> product Category field Shoes -> Men Shoes
    description -> descriptive feature of the product.
    confirmed -> format(bool): permission based on display
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='product_owner')

    name = models.CharField(max_length=120, verbose_name=_("Product Name"),
                            unique=True)

    slug = models.SlugField(max_length=120, verbose_name=_("Product Slug"))

    category = TreeManyToManyField(ProductCategory,
                                 related_name='product-cat')

    description = models.TextField(verbose_name=_("Product Description"))

    confirmed = models.BooleanField(default=False, verbose_name="Product Availability",
                                    help_text=_("format: bool, true == 'product available' "))

    @property
    def get_all_categories(self):
        return [cat.name for cat in self.category]

class Brand(models.Model):
    """
    Product Brand Names Like
    """
    name = models.CharField(max_length=120, verbose_name=_("Product Name"),
                            unique=True)
    slug = models.SlugField(max_length=120, verbose_name=_("Product Slug"))


class ProductType(models.Model):
    """
    Product Type =>
    """
    name = models.CharField(max_length=120, verbose_name=_("Product Name"),
                            unique=True)
    slug = models.SlugField(max_length=120, verbose_name=_("Product Slug"))


class ProductAttribute(models.Model):
    """
    Table for Product Attributes like size, color, weight,  and many more
    """
    name = models.CharField(max_length=140, unique=True)
    description = models.TextField()


class ProductAttributeValue(models.Model):
    """
    Table for Product Attribute Value associated with Product and Product Attributes
    with attribute value format of Product Attribute => Product Attribute Values.
    Size => 10, 11
    color => red, green, blue

    """
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE,
                                          related_name='product_attribute')
    attribute_value = models.CharField(max_length=100, verbose_name=_("Attribute Value"))


class ProductStore(BaseModel):
    """
    Product Inventory/Store
    Price Information, Brand, sku, availability, discount price, sell price,
    store price, retail price etc.
    """
    class ActiveProductQuerySet(models.QuerySet):
        """
        Custom created Querysets Manager
        available => filters all products available only
        discounted => filters all available products with discount value
        """
        def available(self):
            return self.filter(confirmed=True)

        def discounted(self):
            return self.available.filter(discount_percentage__gte=0.00)

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
    attribute_val = models.ManyToManyField(ProductAttributeValue, related_name='product_attr_val',
                                           verbose_name=_("Product Attribute Value"))
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

    product_att_val = models.ManyToManyField(ProductAttributeValue,
                                             verbose_name=_("Product Attribute Value"))

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
    discount_percentage = models.DecimalField(max_digits=3, verbose_name=_("Discount Percentage"),
                                              help_text=_("format: required, 0.1 == 10%,"))

    weight = models.DecimalField(decimal_places=2, max_digits=7, verbose_name=_("Product Weight"))
    weight_type = models.CharField(max_length=12, verbose_name=_("Weight Type"),
                                   help_text=_("format: required, type: 'choice', type: kg, g, mg"))


    active = ActiveProductQuerySet.as_manager()


class ProductImage(models.Model):
    """
    Table for multiple Image of a product
    Boolean True save an Image as the Cover Image

    """

    product_inventory = models.ForeignKey(ProductStore, on_delete=models.CASCADE,
                            related_name='product_image')
    image = models.ImageField(blank=True, null=True, verbose_name=_("Product Image"),
                              upload_to='images', help_text=_("format: required, file type: jpg and png"))

    alt_text = models.CharField(max_length=100, verbose_name=_("Alternative Text"),
                                help_text=_("format: `str` __repr__: image text display if image doesn't load"))

    main_image = models.BooleanField(default=False, verbose_name=_("Product Cover Image"),
        help_text=_("format: required bool, designates if it's the cover image of the product or not"))

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self) -> str:
        return f'{self.product_inventory.name}'


class Stock(models.Model):
    """
    Store Information like all available units of the Product Inventory,
    number of units sold(for Vendors)
    """

    inventory = models.OneToOneField(ProductStore, on_delete=models.CASCADE,
                                     related_name='product_store')
    units = models.PositiveIntegerField(verbose_name=_("Total Available"), default=0,
                                        )
    sold_units = models.PositiveIntegerField(verbose_name=_("Total Available"), default=0,
                                        )

    class Meta:
        verbose_name = "Product Inventory Stock"
        verbose_name_plural = "Products Inventory Stock"

    @property
    def get_available_unit(self):
        return self.units - self.sold_units
