# Generated by Django 4.1.7 on 2023-02-28 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('car_repair_servis', '0013_remove_order_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cars', to=settings.AUTH_USER_MODEL, verbose_name='customer'),
        ),
    ]
