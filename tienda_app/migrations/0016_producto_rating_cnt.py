# Generated by Django 4.2.6 on 2023-12-08 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda_app', '0015_producto_rating_avg'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='rating_cnt',
            field=models.IntegerField(default=0),
        ),
    ]