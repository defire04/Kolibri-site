import sys
from PIL import Image
from io import BytesIO
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import  reverse

User = get_user_model()

def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})



class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass

# 1 Product
# 2 Category
# 3 CartProduct
# 4 Cart
# 5 Order
# ************************
# 6 Customer
# 7 Specification


class LatestProductsManager:
    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True)
        return products


class LatestProducts:

    object = LatestProductsManager()


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    MIN_RESOLUTION = (300, 300)
    MAX_RESOLUTION = (450, 300)
    MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    descripytion = models.TextField(verbose_name='Описание', null=True)
    # price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        # image = self.image
        # img = Image.open(image)
        # min_height, min_width = self.MIN_RESOLUTION
        # max_height, max_width = self.MAX_RESOLUTION
        #
        #   # Для контроля размера фотографий
        # if img.height < min_height or img.width < min_width:
        #    raise MinResolutionErrorException('Разрешение изображение меньше минимального разрешения!')
        # if img.height > max_height or img.width > max_width:
        #    raise MaxResolutionErrorException('Разрешение изображение больше максимального разрешения!')
        #
        # print(img.width, img.height)

        image = self.image
        img = Image.open(image)
        new_img = img.convert('RGB')
        resized_new_img = new_img.resize((450, 300), Image.ANTIALIAS)
        filestream = BytesIO()
        resized_new_img.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        name ='{}.{}'.format(*self.image.name.split('.'))
        # print(self.image.name)
        self.image = InMemoryUploadedFile(filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None)
        super().save(*args, **kwargs)

class Loader(Product):

    сarrying = models.CharField(max_length=255, verbose_name='Вантажопідйомність, кг')
    mast_lifting_height = models.CharField(max_length=255, verbose_name='Висота підйому мачти, мм')
    length_of_forks = models.CharField(max_length=255, verbose_name='Довжина вил, мм')
    engine_type = models.CharField(max_length=255, verbose_name='Тип двигателя')
    state = models.CharField(max_length=255, verbose_name='Стан')
    weight = models.CharField(max_length=255, verbose_name='Вага')

    def __str__(self):
     return "{} : {}".format(self.category.name, self.title)

    def get_absplute_url(self):
        return get_product_url(self, 'product_detail')


class ElectricCarts(Product):

    # сarrying = models.CharField(max_length=255, verbose_name='Вантажопідйомність, кг')
    # mast_lifting_height = models.CharField(max_length=255, verbose_name='Висота підйому, мм')
    # length_of_forks = models.CharField(max_length=255, verbose_name='Довжина вил, мм')

    сarrying = models.CharField(max_length=255, verbose_name='Вантажопідйомність, кг')
    # battery = models.CharField(max_length=255, verbose_name='Характеристики акамулятора ')
    weight = models.CharField(max_length=255, verbose_name='Власна масса, кг')
    turning_radius = models.CharField(max_length=255, verbose_name='Радіус повороту, мм')

    def __del__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absplute_url(self):
        return get_product_url(self, 'product_detail')


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


# class Specification(models.Model):
#
#    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#    object_id = models.PositiveIntegerField()
#    name = models.CharField(max_length=255, verbose_name='Название товара для характеристик')
#
#    def __str__(self):
#        return "Характеристики для товара: {}".format(self.name)
