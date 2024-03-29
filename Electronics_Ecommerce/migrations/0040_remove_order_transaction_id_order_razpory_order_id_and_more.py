# Generated by Django 4.2.1 on 2023-06-11 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics_Ecommerce', '0039_order_delivery_decription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='order',
            name='razpory_order_id',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razpory_payment_id',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razpory_signature_id',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]
