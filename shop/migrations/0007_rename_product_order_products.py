# Generated by Django 3.2 on 2021-05-04 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20210504_1333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='products',
        ),
    ]
