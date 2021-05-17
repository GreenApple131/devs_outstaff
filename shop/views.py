from django.views.generic import ListView, DetailView, FormView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.core import serializers
from random import randint
import json

from account.models import Profile
from . import models
from . import forms
# Create your views here.


def create_order_number(n):
    return n+1


class HeaderSearchView(View):
    model = models.Product
    template_name = "shop/shop_header.html"

    def post(self, *args, **kwargs):
        searched_str = json.loads(self.request.body).get('searchBar')
        print('searched_str', searched_str)

        products = models.Product.objects.filter(
            name__icontains=searched_str
        )[:5]
        p_val = products.values('id', 'name')
        data = []
        i = 0
        for product in p_val:
            obj = {
                'id': product['id'],
                'name': product['name'],
                'absolute_url': products[i].get_absolute_url()
            }
            data.append(obj)
            i += 1
        return JsonResponse({'data': data})


class ProductListView(ListView):
    model = models.Product
    queryset_products = models.Product.objects.all()

    paginate_by = 3

    context_object_name = 'product_list'
    template_name = "shop/shop.html"


class ProductDetailView(DetailView):
    model = models.Product
    context_object_name = 'object'
    template_name = "shop/product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_products = models.Product.objects.all()
        context['product_list'] = queryset_products
        return context


class ProductCreateView(CreateView):
    model = models.Product
    fields = ['name', 'price', 'category', 'description', 'image', 'available']
    template_name = 'shop/product-form.html'
    success_url = 'shop:shop'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = 'create'
        return context


class ProductUpdateView(UpdateView):
    model = models.Product
    fields = ['name', 'price', 'category', 'description', 'image', 'available']
    template_name = 'shop/product-form.html'
    success_url = 'shop:shop'

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


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        try:
            form = forms.CheckoutForm()
            context = {
                'form': form,
            }
            return render(self.request, 'shop/checkout.html', context)
        except ObjectDoesNotExist:
            messages.warning(
                self.request, "You do not have items in your cart!")
            return redirect('shop:shop')

    def post(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        cart = models.Cart.objects.filter(customer=profile)
        billing_qs = models.BillingData.objects.filter(customer=profile)

        form = forms.CheckoutForm(self.request.POST or None)
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                phone_number = form.cleaned_data.get('phone_number')
                email = form.cleaned_data.get('email')
                city = form.cleaned_data.get('city')
                delivery = form.cleaned_data.get('delivery')
                payment_option = form.cleaned_data.get('payment_option')

                if billing_qs.exists():
                    models.BillingData.objects.filter(customer=profile).update(
                        customer=profile,
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                        email=email,
                        city=city,
                        delivery=delivery
                    )
                else:
                    models.BillingData.objects.create(
                        customer=profile,
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                        email=email,
                        city=city,
                        delivery=delivery
                    )

                ordered_product = models.OrderedProduct.objects.last()
                if ordered_product is None:
                    order_number = 1
                else:
                    order_number = create_order_number(
                        ordered_product.order_number)

                order = models.Order.objects.create(
                    customer=profile,
                    billing_data=models.BillingData.objects.get(
                        customer=profile),
                    order_number=order_number
                )

                for p in cart:
                    o_product = models.OrderedProduct.objects.create(
                        order_number=order_number,
                        copy_of_product=p.product,
                        quantity=p.quantity
                    )
                    order.ordered_product.add(o_product)

                cart.delete()

                messages.success(self.request, "Thanks, order created!")
                return redirect('shop:shop')
            else:
                messages.warning(
                    self.request, "Form is not valid. Please, try again!")
                return redirect('shop:shop')
        except ObjectDoesNotExist:
            messages.warning(
                self.request, "You do not have products in your cart!")
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


class SearchResultsView(ListView):
    model = models.Product
    template_name = 'shop/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = models.Product.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )
        return object_list
