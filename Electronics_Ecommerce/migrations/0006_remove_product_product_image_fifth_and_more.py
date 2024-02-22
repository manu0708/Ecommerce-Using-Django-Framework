# Generated by Django 4.2 on 2023-04-22 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics_Ecommerce', '0005_product_product_slug_alter_product_product_discount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_image_fifth',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_image_fourth',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_image_second',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_image_third',
        ),
        migrations.AlterField(
            model_name='brand',
            name='brands_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='main_category',
            name='main_category_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='products_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product_size_quantity',
            name='product_size_quantity_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='size',
            name='sizes_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sub_category',
            name='sub_category_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]