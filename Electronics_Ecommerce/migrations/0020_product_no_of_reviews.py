# Generated by Django 4.2 on 2023-05-10 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics_Ecommerce', '0019_remove_product_average_review_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='no_of_reviews',
            field=models.IntegerField(default=0),
        ),
    ]
