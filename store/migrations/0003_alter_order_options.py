# Generated by Django 5.0.6 on 2024-09-02 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel order')]},
        ),
    ]