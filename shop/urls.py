from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include

from . import views

app_name = 'shop'

urlpatterns = [
    path('shop/', views.ProductListView.as_view(), name='shop'),
    path('ajax/products-search', views.HeaderSearchView.as_view(), name='ajax-products-search'),
    path('shop/search/', views.SearchResultsView.as_view(), name='search'),
    path('product-create/', views.ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
    
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<int:id>', views.add_to_cart, name='add-to-cart'),
    path('remove-one-from-cart/<int:id>', views.remove_one_from_cart, name='remove-one-from-cart'),
    path('remove-from-cart/<int:id>', views.remove_from_cart, name='remove-from-cart'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
