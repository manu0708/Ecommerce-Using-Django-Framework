# Generated by Django 4.2.1 on 2023-06-01 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Electronics_Ecommerce', '0024_product_featured_product_product_latest_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliverAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliver_name', models.CharField(max_length=50, null=True)),
                ('deliver_mobile_no', models.IntegerField(max_length=10, null=True)),
                ('deliver_pincode', models.IntegerField(max_length=10, null=True)),
                ('deliver_locality', models.CharField(max_length=100, null=True)),
                ('deliver_address', models.TextField(max_length=500, null=True)),
                ('deliver_city', models.CharField(max_length=100, null=True)),
                ('deliver_state', models.CharField(max_length=100, null=True)),
                ('deliver_landmark', models.CharField(max_length=100, null=True)),
                ('deliver_alternative_mobile_no', models.IntegerField(max_length=10, null=True)),
                ('deliver_type', models.CharField(max_length=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
