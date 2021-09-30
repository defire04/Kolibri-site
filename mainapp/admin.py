from django import forms
from django.contrib import admin
from .models import *


class LoaderCategoryChoiceField(forms.ModelChoiceField):
    pass


class ElectricCartsCategoryChoiceField(forms.ModelChoiceField):
    pass


class LoaderAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return LoaderCategoryChoiceField(Category.objects.filter(slug='loader'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ElectricCartsAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ElectricCartsCategoryChoiceField(Category.objects.filter(slug='electric carts'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Category)
admin.site.register(Loader, LoaderAdmin)
admin.site.register(ElectricCarts, ElectricCartsAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
