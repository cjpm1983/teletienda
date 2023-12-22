# Generated by Django 4.2.6 on 2023-12-21 21:48

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('tienda_app', '0020_alter_producto_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tienda',
            name='imagen',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='images/default.png', force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[1000, 700], upload_to='tiendas/'),
        ),
    ]
