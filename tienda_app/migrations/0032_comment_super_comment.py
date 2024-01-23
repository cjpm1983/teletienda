# Generated by Django 4.2.6 on 2024-01-22 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tienda_app', '0031_etiqueta_producto_etiquetas'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='super_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='super_comments', to='tienda_app.comment'),
        ),
    ]
