from django.db import models
from datetime import datetime
from account.models import Profile


class Product(models.Model):
    CATEGORY = (
        ('First category', 'First category'),
        ('Second category', 'Second category'),
        ('Third category', 'Third category'),
        ('Fourth category', 'Fourth category')
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class OrderedProduct(models.Model):
    customer = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivering', 'Delivering'),
        ('Delivered', 'Delivered')
    )

    customer = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    product = models.ManyToManyField(OrderedProduct)
    ordered_date = models.DateTimeField(default=datetime.now, null=True)
    status = models.CharField(
        max_length=200, null=True, choices=STATUS, default='Pending')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return '{} ordered in {}'.format(self.customer.user.username, self.ordered_date)
