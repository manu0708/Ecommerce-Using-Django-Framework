# Generated by Django 4.2.1 on 2023-06-10 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics_Ecommerce', '0038_order_delivery_expected_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_decription',
            field=models.CharField(blank=True, default='Delivery expected on', max_length=50, null=True),
        ),
    ]