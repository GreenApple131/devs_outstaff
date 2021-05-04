from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include

from . import views

app_name = 'shop'

urlpatterns = [
    path('shop/', views.ProductListView.as_view(), name='shop'),
    path('product-create/', views.ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
    
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<int:id>', views.add_to_cart, name='add-to-cart'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
