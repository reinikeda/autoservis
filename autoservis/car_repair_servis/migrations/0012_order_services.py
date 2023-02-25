# Generated by Django 4.1.7 on 2023-02-25 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_repair_servis', '0011_remove_carmodel_engine_remove_carmodel_year_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='services',
            field=models.ManyToManyField(help_text='select service(s) for this order', to='car_repair_servis.service', verbose_name='service(s)'),
        ),
    ]