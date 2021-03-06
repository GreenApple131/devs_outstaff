# Generated by Django 3.2.3 on 2021-06-02 16:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entries',
            old_name='owner',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='entries',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.CreateModel(
            name='EntriesStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_number', models.DecimalField(decimal_places=4, max_digits=4, null=True)),
                ('amount_of_entries', models.DecimalField(decimal_places=4, max_digits=4, null=True)),
                ('total_distance', models.FloatField(null=True)),
                ('total_duration', models.DurationField()),
                ('weekly_average_speed', models.FloatField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
