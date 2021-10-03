from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import *


class LoaderAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red; font-size:14px"> При загрузки изображения с разрешением больше {}x{} оно будет обрезано!</span'
            .format(*Product.MAX_RESOLUTION))



    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION

        # Для контроля размера  и разрешения фотографий
        if  image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не должен превышать 3МБ!')

        if img.height < min_height or img.width < min_width:
           raise ValidationError('Разрешение изображение меньше минимального разрешения!')
        if img.height > max_height or img.width > max_width:
           raise ValidationError('Разрешение изображение больше максимального разрешения!')  

        #print(img.width, img.height)
        return image


class LoaderAdmin(admin.ModelAdmin):

    form = LoaderAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='loader'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ElectricCartsAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='electric_carts'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Category)
admin.site.register(Loader, LoaderAdmin)
admin.site.register(ElectricCarts, ElectricCartsAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
