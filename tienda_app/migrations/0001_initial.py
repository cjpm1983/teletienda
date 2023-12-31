# Generated by Django 4.2.6 on 2023-10-16 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=20)),
                ('encargado', models.CharField(max_length=100)),
                ('provincia', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreProducto', models.CharField(max_length=100)),
                ('foto', models.ImageField(upload_to='productos/')),
                ('cantidad', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unidad', models.CharField(max_length=20)),
                ('descripcion', models.TextField()),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda_app.tienda')),
            ],
        ),
    ]
