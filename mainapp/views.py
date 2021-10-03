from django.shortcuts import render
from django.views.generic import DetailView
from .models import Loader, ElectricCarts

def test_view(request):
    return render(request, 'base.html', {})


class ProductDetailViev(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'loader': Loader,
        'electric_carts' : ElectricCarts,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    # model = Model
    # queryset = Model.objects.all()
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'
