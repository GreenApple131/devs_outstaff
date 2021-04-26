from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from . import forms
from .models import Product
# Create your views here.


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'object'
    template_name = "shop/product-detail.html"


class ProductListView(ListView):
    form_class = forms.ProductForm
    model = Product
    queryset_products = Product.objects.all()
    template_name = "shop/shop.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context['product_list'] = self.queryset_products

        create_form = self.form_class()
        context['create_form'] = create_form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        create_form = self.form_class(request.POST)

        if create_form.is_valid():
            create_form.save()
        return render(request, self.template_name, {'create_form': create_form})
