# Generated by Django 4.2.6 on 2024-02-06 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Preferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=100, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('vnumerico', models.IntegerField(blank=True, null=True, verbose_name='Valor si es un número')),
                ('vtexto', models.CharField(blank=True, max_length=255, null=True, verbose_name='Valor si es un texto')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'Preferencias',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreProducto', models.CharField(max_length=100)),
                ('foto', django_resized.forms.ResizedImageField(blank=True, crop=None, default='images/default.png', force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[1000, 700], upload_to='productos/')),
                ('cantidad', models.IntegerField(blank=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unidad', models.CharField(blank=True, max_length=20)),
                ('descripcion', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('visible', models.BooleanField(default=True, help_text='Si el producto es visible se mostrará en la tienda online.', verbose_name='Visible')),
                ('rating_avg', models.FloatField(default=0)),
                ('rating_cnt', models.IntegerField(default=0)),
                ('etiquetas', models.ManyToManyField(to='tienda_app.etiqueta')),
                ('likes', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'productos',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_username', models.CharField(blank=True, max_length=50)),
                ('uri_token', models.CharField(blank=True, max_length=255)),
                ('confirmation_token', models.CharField(blank=True, max_length=255)),
                ('avatar', django_resized.forms.ResizedImageField(blank=True, crop=None, default='images/default.png', force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[1000, 700], upload_to='avatars/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('imagen', django_resized.forms.ResizedImageField(blank=True, crop=None, default='tiendas/default.png', force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[1000, 700], upload_to='tiendas/')),
                ('descripcion', models.TextField(blank=True)),
                ('direccion', models.CharField(blank=True, max_length=100)),
                ('correo', models.EmailField(blank=True, max_length=254)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('encargado', models.CharField(blank=True, max_length=100)),
                ('ciudad', models.CharField(blank=True, max_length=100)),
                ('provincia', models.CharField(blank=True, choices=[('pinar_del_rio', 'Pinar del Río'), ('artemisa', 'Artemisa'), ('la_habana', 'La Habana'), ('mayabeque', 'Mayabeque'), ('matanzas', 'Matanzas'), ('cienfuegos', 'Cienfuegos'), ('villa_clara', 'Villa Clara'), ('sancti_spiritus', 'Sancti Spíritus'), ('ciego_de_avila', 'Ciego de Ávila'), ('camaguey', 'Camagüey'), ('las_tunas', 'Las Tunas'), ('granma', 'Granma'), ('holguin', 'Holguín'), ('santiago_de_cuba', 'Santiago de Cuba'), ('guantanamo', 'Guantánamo')], max_length=100)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('managers', models.ManyToManyField(blank=True, related_name='managed_tiendas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda_app.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='tienda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda_app.tienda'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_comment', models.BooleanField(default=False)),
                ('super_comment', models.IntegerField(blank=True, null=True)),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda_app.comment')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='tienda_app.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
