# Generated by Django 5.0.6 on 2024-06-06 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['last_name', 'first_name']},
        ),
    ]
