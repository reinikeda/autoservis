# Generated by Django 4.1.7 on 2023-02-22 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_repair_servis', '0005_remove_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_order_sum',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='total order sum'),
        ),
    ]
