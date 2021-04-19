from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.conf import settings
# Create your models here.


# Exteded user model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='customers/')
    birth_date = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
