# Generated by Django 3.2.3 on 2021-06-02 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_auto_20210602_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='entries',
            name='week_number',
            field=models.PositiveIntegerField(null=True),
        ),
    ]