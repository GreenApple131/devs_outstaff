from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    # используя prepopulated_fields, мы настраиваем поле slug так, чтобы его значение формировалось автоматически из поля name


# Register your models here.
# admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Order)
admin.site.register(models.Cart)
admin.site.register(models.Tag)
