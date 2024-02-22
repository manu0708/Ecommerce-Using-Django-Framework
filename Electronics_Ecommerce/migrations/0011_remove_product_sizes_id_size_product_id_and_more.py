# Generated by Django 4.2 on 2023-04-26 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics_Ecommerce', '0010_rename_product_reviews_product_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sizes_id',
        ),
        migrations.AddField(
            model_name='size',
            name='product_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]