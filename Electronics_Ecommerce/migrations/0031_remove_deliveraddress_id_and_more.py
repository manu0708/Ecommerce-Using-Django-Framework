# Generated by Django 4.2.1 on 2023-06-01 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics_Ecommerce', '0030_alter_deliveraddress_deliver_alternative_mobile_no_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveraddress',
            name='id',
        ),
        migrations.AddField(
            model_name='deliveraddress',
            name='deliver_address_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
    ]