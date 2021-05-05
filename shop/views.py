from django.views.generic import ListView, DetailView, FormView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from account.models import Profile
from . import models
# Create your views here.


class ProductDetailView(DetailView):
    model = models.Product
    context_object_name = 'object'
    template_name = "shop/product-detail.html"


class ProductListView(ListView):
    model = models.Product
    queryset_products = models.Product.objects.all()

    paginate_by = 3

    context_object_name = 'product_list'
    template_name = "shop/shop.html"


class ProductCreateView(CreateView):
    model = models.Product
    fields = ['name', 'price', 'category', 'description', 'image', 'available']
    template_name = 'shop/product-form.html'
    success_url = '/shop/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = 'create'
        return context


class ProductUpdateView(UpdateView):
    model = models.Product
    fields = ['name', 'price', 'category', 'description', 'image', 'available']
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


class CartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            cart = models.Cart.objects.filter(customer=profile)
            total_price = 0
            for product in cart.all():
                total_price += product.get_products_price()

            context = {
                'object': cart,
                'total_price': total_price,
            }
            return render(request, 'shop/cart.html', context)
        except ObjectDoesNotExist:
            context = {
                'object': ''
            }
            messages.warning(request, "You do not have an active order")
            # return render(request, 'shop/cart.html', context)
            return redirect('shop:shop')


def add_to_cart(request, id):
    product = get_object_or_404(models.Product, id=id)
    profile = Profile.objects.get(user=request.user)
    ordered_product = models.Cart.objects.filter(
        customer=profile,
        product=product,
    )

    if ordered_product.exists():
        cart = ordered_product[0]
        cart.quantity += 1
        cart.save()

        messages.success(request, 'Product quantity was updated!')
        return redirect('shop:cart')
    else:
        ordered_product = models.Cart.objects.create(
            customer=profile,
            product=product
        )

        messages.success(request, 'Product has been added to cart!')
        return redirect('shop:cart')


def remove_one_from_cart(request, id):
    product = get_object_or_404(models.Product, id=id)
    profile = Profile.objects.get(user=request.user)
    ordered_product = models.Cart.objects.filter(
        customer=profile,
        product=product,
    )

    if ordered_product.exists():
        cart = ordered_product[0]

        if cart.quantity == 1:
            return remove_from_cart(request, id)
        else:
            cart.quantity -= 1

        cart.save()

        messages.success(request, 'Product quantity was updated!')
        return redirect('shop:cart')
    else:
        messages.error(request, 'Product was not in your cart!')
        return redirect('shop:cart')


def remove_from_cart(request, id):
    model_product = get_object_or_404(models.Product, id=id)
    profile = Profile.objects.get(user=request.user)
    ordered_product = models.Cart.objects.filter(
        customer=profile,
        product=model_product,
    )
    if ordered_product.exists():
        ordered_product = ordered_product[0]
        ordered_product.delete()

        messages.success(request, 'Product quantity was deleted!')
        return redirect('shop:cart')
    else:

        messages.error(request, 'Product was not in your cart!')
        return redirect('shop:cart')
