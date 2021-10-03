from django.urls import path
from .views import test_view, ProductDetailViev


urlpatterns = [
    path('', test_view, name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailViev.as_view(), name='product_detail'),

]
