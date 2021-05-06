# Generated by Django 3.2 on 2021-05-06 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_auto_20210506_0813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_number',
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='order_number',
            field=models.PositiveIntegerField(default=1, unique=True),
        ),
    ]
