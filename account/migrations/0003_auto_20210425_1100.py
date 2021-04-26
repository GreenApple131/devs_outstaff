# Generated by Django 3.2 on 2021-04-25 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_order_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedproduct',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='orderedproduct',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderedProduct',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]