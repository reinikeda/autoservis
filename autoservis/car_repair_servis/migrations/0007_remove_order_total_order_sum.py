# Generated by Django 4.1.7 on 2023-02-22 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car_repair_servis', '0006_order_total_order_sum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_order_sum',
        ),
    ]
