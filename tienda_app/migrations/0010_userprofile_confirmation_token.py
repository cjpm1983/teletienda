# Generated by Django 4.2.6 on 2023-11-09 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda_app', '0009_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='confirmation_token',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
