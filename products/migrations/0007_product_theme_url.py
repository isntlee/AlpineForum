# Generated by Django 4.2.10 on 2024-02-22 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_rename_image_product_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='theme_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
