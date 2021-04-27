from django.contrib import admin
from django.urls import path, re_path, include

from . import views


urlpatterns = [
    path('shop/', views.ProductListView.as_view(), name='shop'),
    path('product-create/', views.ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product-delete'),

]