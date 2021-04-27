from django.views.generic import ListView, DetailView, FormView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from . import models
# Create your views here.


class ProductDetailView(DetailView):
    model = models.Product
    context_object_name = 'object'
    template_name = "shop/product-detail.html"


class ProductListView(ListView):
    model = models.Product
    queryset_products = models.Product.objects.all()

    paginate_by = 5

    context_object_name = 'product_list'
    template_name = "shop/shop.html"


class ProductCreateView(CreateView):
    model = models.Product
    fields = ['name', 'price', 'category', 'description']
    template_name = 'shop/product-form.html'
    success_url = '/shop/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = 'create'
        return context


class ProductUpdateView(UpdateView):
    model = models.Product
    fields = ['name', 'price', 'category', 'description']
    template_name = 'shop/product-form.html'
    success_url = '/shop/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = 'update'
        return context


class ProductDeleteView(DeleteView):
    model = models.Product
    template_name = 'shop/confirm-delete.html'
    success_url = reverse_lazy('shop')
