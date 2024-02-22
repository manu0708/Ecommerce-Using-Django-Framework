from djmoney.models.fields import MoneyField
from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_avatar = models.ImageField(upload_to="user_profile")
    mobile_no = models.IntegerField(null=True, blank=True, default=0)
    gender = models.CharField(max_length=50, null=True, blank=True, default='')
    otp = models.IntegerField(default=0)

class main_category(models.Model):
    main_category_id = models.AutoField(primary_key=True)
    main_category_name = models.CharField(max_length=50)
    main_category_image = models.ImageField(upload_to="images", default='images/img1.jpg')
    def __str__(self):
        return self. main_category_name


class brand(models.Model):
    brands_id = models.AutoField(primary_key=True)
    brands_name = models.CharField(max_length=50)

    def __str__(self):
        return self.brands_name


class category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    category_image = models.ImageField(upload_to="images", default='images/img1.jpg')
    main_category_id = models.ForeignKey(
        main_category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name


class sub_category(models.Model):
    sub_category_id = models.AutoField(primary_key=True)
    sub_category_name = models.CharField(max_length=50)
    category_id = models.ForeignKey(category, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_category_name


class product(models.Model):
    products_id = models.AutoField(primary_key=True)
    products_name = models.CharField(max_length=50)
    products_title = models.CharField(max_length=50)
    product_slug = models.SlugField(unique=True)
    products_price = MoneyField(
        max_digits=19, decimal_places=0, default_currency='INR')
    products_selling_price = MoneyField(
        max_digits=19, decimal_places=0, default_currency='INR')
    product_discount = models.CharField(max_length=20)
    product_description = models.TextField(max_length=500)
    product_image_first = models.ImageField(
        upload_to='images/', max_length=255)
    free_delivery = models.BooleanField()
    cash_on_delivery = models.BooleanField()
    product_return = models.BooleanField()
    product_average = models.DecimalField(
        null=True, editable=False, decimal_places=1, max_digits=3)
    no_of_reviews = models.IntegerField(default=0)
    featured_product = models.BooleanField(default=False)
    latest_product = models.BooleanField(default=False)
    top_rated_product = models.BooleanField(default=False)
    reviewed_product = models.BooleanField(default=False)
    tag = models.CharField(null=True, max_length=20, default='nothing')
    category_id = models.ForeignKey(category, on_delete=models.CASCADE)
    sub_category_id = models.ForeignKey(sub_category, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(brand, on_delete=models.CASCADE)
    main_category_id = models.ForeignKey(
        main_category, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return self.products_name


class size(models.Model):
    sizes_id = models.AutoField(primary_key=True)
    sizes_name = models.CharField(max_length=50)
    category_id = models.ForeignKey(category, on_delete=models.CASCADE)
    sub_category_id = models.ForeignKey(sub_category, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(brand, on_delete=models.CASCADE)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)

    def __str__(self):
        return self.sizes_name


class Product_Image(models.Model):
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', max_length=255)

    def __str__(self):
        return self.product_id.products_name


class product_size_quantity(models.Model):
    product_size_quantity_id = models.AutoField(primary_key=True)
    products_id = models.ForeignKey(product, on_delete=models.CASCADE)
    sizes_id = models.ForeignKey(size, on_delete=models.CASCADE)
    size_quantity = models.CharField(max_length=50)

    def __str__(self):
        return self.size_quantity


class Reviews(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField()

    # def __str__(self):
    #     return f'{self.user_id.first_name} {self.product_id.products_name}'


class Addtocart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = MoneyField(
        max_digits=19, decimal_places=2, default_currency='INR', default="500")
    created_at = models.DateTimeField()

class DeliverAddress(models.Model):
    deliver_address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deliver_name = models.CharField(max_length=50, null=True, blank=True)
    deliver_mobile_no = models.IntegerField(null=True, blank=True, default=None)
    deliver_pincode = models.IntegerField(null=True, blank=True, default=None)
    deliver_locality = models.CharField(max_length=100, null=True, blank=True)
    deliver_address = models.TextField(max_length=500, null=True, blank=True)
    deliver_city = models.CharField(max_length=100, null=True, blank=True)
    deliver_state = models.CharField(max_length=100, null=True, blank=True)
    deliver_landmark = models.CharField(max_length=100, null=True, blank=True)
    deliver_alternative_mobile_no = models.IntegerField(null=True, blank=True, default=None)
    deliver_type = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.deliver_name
    

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_product = models.ForeignKey(product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=0)
    amount = MoneyField(
        max_digits=19, decimal_places=0, default_currency='INR', default=0)
    email = models.EmailField(default="")
    address = models.TextField(max_length=500)
    razpory_order_id = models.CharField(default='', null=True, blank=True, max_length=500)
    razpory_payment_id = models.CharField(default='', null=True, blank=True, max_length=500)
    razpory_signature_id = models.CharField(default='', null=True, blank=True, max_length=500)
    payment_mode = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    order_status = models.CharField(max_length=50, null=True, blank=True, default="")
    delivery_decription = models.CharField(max_length=50, null=True, blank=True, default='Delivery expected on')
    Delivery_expected = models.DateField(null=True, blank=True)
    order_date_time = models.DateTimeField(default=datetime.datetime.now)
    pincode = models.IntegerField(default=0)

class Image_slider(models.Model):
    slider_image = models.ImageField(upload_to='Image_slider')
    slider_text = models.CharField(max_length=100)
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)

class Complaint(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    mobile = models.IntegerField()
    message = models.TextField(max_length=1000)