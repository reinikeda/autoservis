# Generated by Django 4.1.7 on 2023-02-21 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_repair_servis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='year',
            field=models.IntegerField(verbose_name='year'),
        ),
    ]
