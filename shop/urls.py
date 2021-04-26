from django.contrib import admin
from django.urls import path, re_path, include

from . import views


urlpatterns = [
    path('shop/', views.ProductListView.as_view(), name='shop'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

]