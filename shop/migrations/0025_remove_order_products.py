# Generated by Django 3.2 on 2021-05-06 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_auto_20210506_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
    ]
