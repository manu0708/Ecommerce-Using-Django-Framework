from django.contrib import admin
from .models import *

class user_profile(admin.ModelAdmin):
    list_display = ("user", "user_avatar")

class maincategory(admin.ModelAdmin):
    list_display = ("main_category_id", "main_category_name", "main_category_image")


class Brands(admin.ModelAdmin):
    list_display = ("brands_id", "brands_name")


class categorys(admin.ModelAdmin):
    list_display = ("category_id", "category_name", "category_image","main_category_id")


class subcategory(admin.ModelAdmin):
    list_display = ("sub_category_id", "category_id", "sub_category_name")


class Products(admin.ModelAdmin):
    list_display = ("products_name", "products_price", "products_selling_price", "product_discount",
                    "main_category_id", "product_average", "no_of_reviews", "featured_product", "latest_product", "top_rated_product", "reviewed_product", "tag","category_id", "sub_category_id", "brand_id", "free_delivery", "cash_on_delivery", "product_return", "product_image_first")


class Product_Images(admin.ModelAdmin):
    list_display = ("product_id", "image")


class sizes(admin.ModelAdmin):
    list_display = ("sizes_id", "brand_id",
                    "category_id", "sub_category_id", "product_id", "sizes_name")


class Product_Quantity(admin.ModelAdmin):
    list_display = ("product_size_quantity_id", "products_id",
                    "sizes_id", "size_quantity")


class Review(admin.ModelAdmin):
    list_display = ("user_id", "product_id", "comment", "rating", "created_at")


class addtocart(admin.ModelAdmin):
    list_display = ("user_id", "product", "quantity", "created_at")

class deliver_address(admin.ModelAdmin):
    list_display = ("user", "deliver_name", "deliver_mobile_no", "deliver_pincode", "deliver_locality", "deliver_address", "deliver_city", "deliver_state", "deliver_landmark", "deliver_alternative_mobile_no", "deliver_type")

class orders(admin.ModelAdmin):
    list_display = ("order_id", "user", "ordered_product", "product_quantity", "amount", "email", "address", "razpory_order_id", "payment_mode", "payment_status", "pincode","order_status", "delivery_decription","Delivery_expected", "order_date_time")

class image_slider(admin.ModelAdmin):
    list_display = ('slider_text', 'slider_image')

class wishlist(admin.ModelAdmin):
    list_display = ('user', 'product')

class complaint(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile', 'message')

# Register your models here.
admin.site.register(Profile, user_profile)
admin.site.register(main_category, maincategory)
admin.site.register(brand, Brands)
admin.site.register(category, categorys)
admin.site.register(sub_category, subcategory)
admin.site.register(size, sizes)
admin.site.register(product, Products)
admin.site.register(Product_Image, Product_Images)
admin.site.register(product_size_quantity, Product_Quantity)
admin.site.register(Reviews, Review)
admin.site.register(Addtocart, addtocart)
admin.site.register(DeliverAddress, deliver_address)
admin.site.register(Order, orders)
admin.site.register(Image_slider, image_slider)
admin.site.register(Wishlist, wishlist)
admin.site.register(Complaint, complaint)