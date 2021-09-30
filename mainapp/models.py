import sys
from io import BytesIO
from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()



# 1 Product
# 2 Category
# 3 CartProduct
# 4 Cart
# 5 Order
# ************************
# 6 Customer
# 7 Specification


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    descripytion = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title


class Loader(Product):

    сarrying = models.CharField(max_length=255, verbose_name='Вантажопідйомність, кг')
    mast_lifting_height = models.CharField(max_length=255, verbose_name='Висота підйому мачти, мм')
    length_of_forks = models.CharField(max_length=255, verbose_name='Довжина вил, мм')
    engine_type = models.CharField(max_length=255, verbose_name='Тип двигателя')
    state = models.CharField(max_length=255, verbose_name='Стан')
    weight = models.CharField(max_length=255, verbose_name='Вага')

    def __str__(self):
     return "{} : {}".format(self.category.name, self.title)


class ElectricCarts(Product):

    сarrying = models.CharField(max_length=255, verbose_name='Вантажопідйомність, кг')
    mast_lifting_height = models.CharField(max_length=255, verbose_name='Висота підйому, мм')
    length_of_forks = models.CharField(max_length=255, verbose_name='Довжина вил, мм')

    def __del__(self):
        return "{} : {}".format(self.category.name, self.title)


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    # product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE) замена на content_type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} для корзины".format(self.product.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


#class Specification(models.Model):
#
#    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#    object_id = models.PositiveIntegerField()
#    name = models.CharField(max_length=255, verbose_name='Название товара для характеристик')
#
#    def __str__(self):
#        return "Характеристики для товара: {}".format(self.name)
