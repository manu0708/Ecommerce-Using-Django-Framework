# Generated by Django 4.2.1 on 2023-06-10 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics_Ecommerce', '0037_image_slider'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Delivery_expected',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]