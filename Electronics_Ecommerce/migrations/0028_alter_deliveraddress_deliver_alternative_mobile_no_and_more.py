# Generated by Django 4.2.1 on 2023-06-01 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics_Ecommerce', '0027_alter_deliveraddress_deliver_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveraddress',
            name='deliver_alternative_mobile_no',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='deliveraddress',
            name='deliver_mobile_no',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='deliveraddress',
            name='deliver_pincode',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]