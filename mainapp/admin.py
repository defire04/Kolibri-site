from django.forms import ModelChoiceField
from django.contrib import admin
from .models import *


class LoaderAdmin(admin.ModelAdmin):

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
