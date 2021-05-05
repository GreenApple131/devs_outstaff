from django.db import models
from datetime import datetime
from django.shortcuts import reverse
from django.template.defaultfilters import slugify

from account.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, default="test-slug")
    price = models.FloatField(null=True)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    available = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=datetime.now, null=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/product/%i" % self.id

    def get_absolute_update_url(self):
        return "/product/%i/update" % self.id

    def get_absolute_delete_url(self):
        return "/product/%i/delete" % self.id

    def get_add_to_cart_url(self):
        return reverse("shop:add-to-cart", kwargs={
            'id': self.id
        })

    def get_remove_one_from_cart_url(self):
        return reverse("shop:remove-one-from-cart", kwargs={
            'id': self.id
        })

    def get_remove_from_cart_url(self):
        return reverse("shop:remove-from-cart", kwargs={
            'id': self.id
        })


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

    def __str__(self):
        return f"{self.quantity} of {self.product.name} ordered {self.customer.user.username}"

    def get_quantity(self):
        return self.quantity

    def get_products_price(self):
        return self.quantity*self.product.price


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivering', 'Delivering'),
        ('Delivered', 'Delivered')
    )

    customer = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    products = models.ManyToManyField(Cart)
    ordered_date = models.DateTimeField(default=datetime.now, null=True)
    status = models.CharField(
        max_length=200, null=True, choices=STATUS, default='Pending')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return '{} ordered in {}'.format(self.customer.user.username, self.ordered_date)
