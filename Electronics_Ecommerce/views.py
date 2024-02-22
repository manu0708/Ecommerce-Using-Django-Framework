from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import product, category, Reviews, main_category, size, Addtocart, DeliverAddress, Order, Image_slider, Profile, Wishlist, Complaint
import datetime
from math import ceil
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
#fecting users current locations
import requests
import json
import random
#payment integration
from Ecommerce.settings import razorpay_id, razorpay_account_id
import razorpay
from django.contrib import messages
from django.core.mail import send_mail
razorpay_client = razorpay.Client(auth=(razorpay_id, razorpay_account_id))

# encryption and decryption
from .encryption_util import *

# Create your views here.
no_of_carts = 0

def index(request):
    main_categorys = main_category.objects.all()
    image_slider = Image_slider.objects.all()
    prod = product.objects.all()
    for i in prod:
        if len(i.product_slug) < 30:
            en_prod = encrypt(i.product_slug)
            i.product_slug = en_prod
            i.save()
    if request.user.is_authenticated:
        user_avater = Profile.objects.get(user=request.user)
    else:
        user_avater=None
    categorys = category.objects.values('category_id', 'category_name', 'category_image', 'main_category_id')
    c = []
    for i in categorys:
        i['encrypt_key'] = encrypt(i['category_id'])
        i['category_id'] = i['category_id']
        c.append(i)
    featured_products = product.objects.filter(featured_product=True)
    latest_products = product.objects.filter(latest_product=True)
    if request.user.is_authenticated:
        no_of_cart = Addtocart.objects.filter(user_id=request.user)
        no_of_carts = no_of_cart.count()
    else:
        no_of_carts = 0
    context={
        'link':'home',
        'main_categorys':main_categorys,
        'categorys':c,
        'no_of_carts':no_of_carts,
        'featured_products':featured_products,
        'latest_products':latest_products,
        'image_sliders':image_slider,
        'user_avater':user_avater,
    }
    return render(request, 'index.html', context)

def home(request):
    # categorys = category.objects.all()
    products = product.objects.all()
    n = len(products)
    slides = n//4 + ceil((n/4) - (n//4))
    ranges = range(1, slides)
    return render(request, 'home.html', {'link': 'home', 'range': ranges, 'product': products})


def Register(request):
    if (request.method == 'POST'):
        user_name = request.POST.get('Username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('confirm_password')
        otp = random.randint(100000, 999999)
        str_otp = str(otp)
        en_otp = encrypt(str_otp)
        
        if (password == password1):
            if (User.objects.filter(username=user_name)).exists():
                print("executed")
                return render(request, 'message.html', {'message': 'Username is taken', 'mestype': 'error', 'suggestion': 'Please try with diffrent username'})
            else:
                print("else")
                user = User.objects.create(username=user_name, email=email)
                user.set_password(password)
                # user.is_active = False
                user.save()
                user_profile = user
                user_avater = "user_profile/default_user_profile_wLAPJge.png"
                profile = Profile.objects.create(user=user_profile, user_avatar=user_avater)
                profile.save()
                sending_mail(otp, email)
                otptype = "register"
                en_email="user"
                return redirect('verifyotp', en_email, otptype, en_otp)
        else:
            return render(request, 'message.html', {'message': 'Password does not match', 'mestype': 'error', 'suggestion': 'Please try again'})

    else:
        return render(request, 'register.html')


def Login(request):
    if (request.method == 'POST'):
        username = request.POST.get('Username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'message.html', {'message': 'Login successfully', 'type': 'home', 'mestype': 'success', 'suggestion': 'Continue for Shopping'})
        else:
            return render(request, 'message.html', {'message': 'User is not valid', 'mestype': 'error', 'suggestion': 'Please try again with valid cedentials'})

    else:
        return render(request, 'login.html', {'link': 'signin'})


def productdetail(request, product_slugs):
    no_of_carts=0
    prod = product.objects.all()
    for i in prod:
            en_prod = decrypt(i.product_slug)
            if en_prod != None:
                i.product_slug = en_prod
                i.save()

    if (request.method == 'POST'):
        user = request.user
        de = decrypt(product_slugs)
        product_id = product.objects.get(product_slug=de)
        comment = request.POST.get('comment')
        if request.POST.get('rating') == "":
            rate = 0
        else:
            rate = request.POST.get('rating')
        cur_time = datetime.datetime.now()

        review = Reviews.objects.create(
            user_id=user, product_id=product_id, comment=comment, rating=rate, created_at=cur_time)
        review.save()
        all_review = Reviews.objects.filter(product_id=product_id)
        tot_rate = 0
        for aver in all_review:
            tot_rate += aver.rating
        average = tot_rate/all_review.count()
        product_id.product_average = average
        product_id.no_of_reviews = all_review.count()
        product_id.save()
        return HttpResponseRedirect('http://127.0.0.1:8000/product/'+product_slugs+'/')

    else:
        if request.user.is_authenticated:
            user_avater = Profile.objects.get(user=request.user)
        else:
            user_avater=None
        if len(product_slugs) >= 35:
            slugs = decrypt(product_slugs)
            slug = slugs
        else:
            slug = product_slugs
        productdetails = product.objects.get(product_slug=slug)
        maincategory = main_category.objects.get(main_category_name="Fashion")
        latest_products = product.objects.filter(latest_product=True)
        related_products = product.objects.filter(
            category_id=productdetails.category_id).exclude(product_slug=slug)
        for i in latest_products:
            if len(i.product_slug) < 30:
                en_prod = encrypt(i.product_slug)
                i.product_slug = en_prod
                i.save() 

        for i in related_products:
            if len(i.product_slug) < 30:
                en_prod = encrypt(i.product_slug)
                i.product_slug = en_prod
                i.save() 
        try:
            if request.user.is_authenticated:
                no_of_cart = Addtocart.objects.filter(user_id=request.user)
                no_of_carts = no_of_cart.count()
            product_review = Reviews.objects.filter(
                product_id=productdetails)
            five_stars = product_review.filter(rating=5)
            five_starss = five_stars.count()
            five_star = 0
            five_star = five_stars.count()/product_review.count()*100
            four_stars = product_review.filter(rating=4)
            four_starss = four_stars.count()
            four_star = 0
            four_star = four_stars.count()/product_review.count()*100
            three_stars = product_review.filter(rating=3)
            three_starss = three_stars.count()
            three_star = 0
            three_star = three_stars.count()/product_review.count()*100

            two_stars = product_review.filter(rating=2)
            two_starss = two_stars.count()
            two_star = 0
            two_star = two_stars.count()/product_review.count()*100
            one_stars = product_review.filter(rating=1)
            one_starss = one_stars.count()
            one_star = 0
            one_star = one_stars.count()/product_review.count()*100
            if User.is_authenticated:
                ordered = Order.objects.filter(user=request.user, ordered_product=productdetails.products_id)
                cur_user = Reviews.objects.filter(user_id=request.user, product_id=productdetails.products_id)
            product_size = size.objects.filter(product_id=productdetails.products_id)
            context = {
                'productdetail': productdetails,
                'review': product_review,
                'maincat': maincategory,
                'size': product_size,
                'cu': cur_user,
                'relproducts': related_products,
                'five': five_star,
                'four': four_star,
                'three': three_star,
                'two': two_star,
                'one': one_star,
                'fives': five_starss,
                'fours': four_starss,
                'threes': three_starss,
                'twos': two_starss,
                'ones': one_starss,
                'no_of_carts':no_of_carts,
                'user_avater':user_avater,
                'latest_products':latest_products,
                'ordered':ordered,
            }
            return render(request, 'productdetails.html', context)
        except Exception:
            if product_review:
                bol = True
            else:
                product_review = "No reviews given Yet"
            product_size = "No any other Sizes"
            cur_user = ""
            return render(request, 'productdetails.html', {'productdetail': productdetails, 'review': product_review, 'size': product_size, 'cu': cur_user, 'relproducts': related_products, 'no_of_carts': no_of_carts, 'user_avater':user_avater, 'latest_products':latest_products })


@login_required(login_url='login')
def Addtocarts(request, pid, loc):
    products = product.objects.get(products_id=pid)
    check_cart = Addtocart.objects.filter(
        product=products, user_id=request.user)
    if check_cart.exists():
        car_pro = Addtocart.objects.get(product=products,user_id=request.user)
        car_pro.quantity += 1
        car_pro.total = car_pro.product.products_selling_price*car_pro.quantity
        car_pro.save()
        messages.success(request, "Updated Your Cart")
    else:
        user = request.user
        prod = products
        qty = 1
        total = products.products_selling_price
        dt = datetime.datetime.now()

        cart_prod = Addtocart.objects.create(
            user_id=user, product=prod, quantity=qty, total=total, created_at=dt)
        cart_prod.save()
        messages.success(request, "Added to Your Cart")
    # return HttpResponseRedirect('http://127.0.0.1:8000/product/'+loc+'/')
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def updatecart(request, pids, sign):
    if sign == "+":
        car_pro = Addtocart.objects.get(product=pids, user_id=request.user)
        car_pro.quantity += 1
        car_pro.total = car_pro.product.products_selling_price*car_pro.quantity
        car_pro.save()
    else:
        car_pro = Addtocart.objects.get(product=pids, user_id=request.user)
        car_pro.quantity -= 1
        car_pro.total = car_pro.product.products_selling_price*car_pro.quantity
        car_pro.save()
        if car_pro.quantity == 0:
            car_pro.delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        user_avater = Profile.objects.get(user=request.user)
    else:
        user_avater=None
    cart_products = Addtocart.objects.filter(user_id=request.user)
    no_of_carts = cart_products.count()
    without_discount_total = 0
    for i in cart_products:
        without_discount_total += i.product.products_price * i.quantity

    savings = 0
    for i in cart_products:
        minus_value = i.product.products_price - i.product.products_selling_price
        minus_value *= i.quantity
        savings += minus_value

    total_price = 0
    for i in cart_products:
        total_price += i.total
    return render(request, 'addtocart.html', {'link':'cart', 'cat_pro': cart_products, 'tot': total_price,'no_of_carts':no_of_carts, 'savings':savings, 'without_discount_total': without_discount_total, 'user_avater':user_avater})


@login_required(login_url='login')
def Remove_cart_product(request, rpid):
    cart_remove = Addtocart.objects.get(product=rpid, user_id=request.user)
    if cart_remove.quantity > 1:
        cart_remove.quantity -= 1
        cart_remove.total -= cart_remove.product.products_selling_price
        cart_remove.save()
    else:
        cart_remove.delete()
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def Checkout(request, order_from):
    if request.user.is_authenticated:
        user_avater = Profile.objects.get(user=request.user)
    else:
        user_avater=None
    if order_from == "addtocart":
        cart_products = Addtocart.objects.filter(user_id=request.user)
        no_of_items = cart_products.count()
        without_discount_total = 0
        for i in cart_products:
            without_discount_total += i.product.products_price

        savings = 0
        for i in cart_products:
            minus_value = i.product.products_price - i.product.products_selling_price
            minus_value *= i.quantity
            savings += minus_value

        total_price = 0
        for i in cart_products:
            total_price += i.total

    else:
        cart_products = product.objects.get(products_id=order_from)
        without_discount_total = cart_products.products_price
        savings = cart_products.products_price - cart_products.products_selling_price
        total_price = cart_products.products_selling_price 
        no_of_items = 1

    
    cart_product = Addtocart.objects.filter(user_id=request.user)
    no_of_carts = cart_product.count()
    deliver_address = DeliverAddress.objects.filter(user=request.user)
    
    
    context = {
        'no_of_carts':no_of_carts,
        'no_of_items':no_of_items,
        'savings':savings,
        'tot':total_price,
        'deliver_address':deliver_address,
        'without_discount_total':without_discount_total,
        'order_from':order_from,
        'user_avater':user_avater
    }
    return render(request, 'checkout.html', context)

@login_required(login_url='login')
def User_current_location(request, order_from):
    if request.user.is_authenticated:
        user_avater = Profile.objects.get(user=request.user)
    else:
        user_avater=None
    ip = requests.get('https://api.ipify.org?format=json')
    ip_as_text = json.loads(ip.text)
    request_location = requests.get('http://ip-api.com/json/' + ip_as_text["ip"])
    get_location = request_location.text
    user_current_location = json.loads(get_location)

    if order_from == "addtocart":
        cart_products = Addtocart.objects.filter(user_id=request.user)
        no_of_items = cart_products.count()
        without_discount_total = 0
        for i in cart_products:
            without_discount_total += i.product.products_price


        savings = 0
        for i in cart_products:
            minus_value = i.product.products_price - i.product.products_selling_price
            minus_value *= i.quantity
            savings += minus_value

        total_price = 0
        for i in cart_products:
            total_price += i.total

    else:
        cart_products = product.objects.get(products_id=order_from)
        without_discount_total = cart_products.products_price
        savings = cart_products.products_price - cart_products.products_selling_price
        total_price = cart_products.products_selling_price 
        no_of_items = 1

    
    cart_product = Addtocart.objects.filter(user_id=request.user)
    no_of_carts = cart_product.count()
    deliver_address = DeliverAddress.objects.filter(user=request.user)

    context = {
        'user_current_location':user_current_location,
        'no_of_carts':no_of_carts,
        'no_of_items':no_of_items,
        'savings':savings,
        'tot':total_price,
        'deliver_address':deliver_address,
        'without_discount_total':without_discount_total,
        'user_avater':user_avater,
        'order_from':order_from,
    }
    return render(request, 'checkout.html', context)

@login_required(login_url='login')
def SaveDeliverAddress(request):
    if(request.method == 'POST'):
        user = request.user
        name = request.POST.get('Dname')
        mobile = request.POST.get('Dmobile')
        if mobile == '':
            mobile = None
        pincode = request.POST.get('Dpincode')
        if pincode == '':
            pincode = None
        locality = request.POST.get('Dlocality')
        address = request.POST.get('Daddress')
        city = request.POST.get('Dcity')
        state = request.POST.get('Dstate')
        landmark = request.POST.get('Dlandmark')
        alternative_mobile = request.POST.get('Dalternative_mobile')
        address_type = request.POST.get('addresstype')
        if alternative_mobile == '':
            alternative_mobile=None
        
        deliver_address = DeliverAddress.objects.create(user=user, deliver_name=name, deliver_mobile_no=mobile,
        deliver_pincode=pincode, deliver_locality=locality, deliver_address=address,deliver_city=city, deliver_state=state,
        deliver_landmark=landmark, deliver_alternative_mobile_no=alternative_mobile, deliver_type=address_type)

        deliver_address.save()

        return redirect(request.META['HTTP_REFERER'])   

@login_required(login_url='login')
def SelectDeliverAddress(request, delid, order_from):
    if request.user.is_authenticated:
        user_avater = Profile.objects.get(user=request.user)
    else:
        user_avater=None
    selected_delivery_address = DeliverAddress.objects.get(deliver_address_id=delid)
    if order_from == "addtocart":
        this_product = None
        cart_products = Addtocart.objects.filter(user_id=request.user)
        no_of_items = cart_products.count()
        without_discount_total = 0
        for i in cart_products:
            without_discount_total += i.product.products_price

        savings = 0
        for i in cart_products:
            minus_value = i.product.products_price - i.product.products_selling_price
            minus_value *= i.quantity
            savings += minus_value

        total_price = 0
        for i in cart_products:
            total_price += i.total

    else:
        cart_products = product.objects.get(products_id=order_from) 
        no_of_items = 1
        #product is adding to the cart after clicking on the buynow
        products = product.objects.get(products_id=order_from)
        check_cart = Addtocart.objects.filter(
        product=products, user_id=request.user)
        if check_cart.exists():
            this_product = Addtocart.objects.get(product=order_from, user_id=request.user)
        else:
            user = request.user
            prod = products
            qty = 1
            total = products.products_selling_price
            dt = datetime.datetime.now()

            cart_prod = Addtocart.objects.create(
                user_id=user, product=prod, quantity=qty, total=total, created_at=dt)
            cart_prod.save()
            this_product = Addtocart.objects.get(product=order_from, user_id=request.user)

        without_discount_total = cart_products.products_price * this_product.quantity
        savings = (cart_products.products_price - cart_products.products_selling_price) * this_product.quantity
        total_price = cart_products.products_selling_price * this_product.quantity
    
    cart_product = Addtocart.objects.filter(user_id=request.user)
    no_of_carts = cart_product.count()
    deliver_address = DeliverAddress.objects.filter(user=request.user)
    
    context = {
        'selected_delivery_address':selected_delivery_address,
        'no_of_carts':no_of_carts,
        'no_of_items':no_of_items,
        'savings':savings,
        'tot':total_price,
        'without_discount_total':without_discount_total,
        'cart_products':cart_products,
        'this_product':this_product,
        'order_from':order_from,
        'delid':delid,
        'user_avater':user_avater
    }
    return render(request, 'checkout.html', context)

@login_required(login_url='login')
def Orders(request, from_order, delid):
    if request.method == 'POST':
        payment_type = request.POST.get('paymentmode')
        deliver_address = DeliverAddress.objects.get(deliver_address_id=delid)
        if(payment_type == 'cod'):
            if from_order == 'addtocart':
                cart_product = Addtocart.objects.filter(user_id=request.user)
                for counter, i in enumerate(cart_product):
                    user = request.user
                    ordered_product = i.product
                    quantity = i.quantity
                    amount = i.product.products_selling_price * i.quantity
                    email = request.user.email
                    address = deliver_address.deliver_name + " " + str(deliver_address.deliver_mobile_no) + " " + deliver_address.deliver_locality + " " + deliver_address.deliver_address + " " + deliver_address.deliver_city + " " + deliver_address.deliver_state + " " + deliver_address.deliver_landmark + " " + str(deliver_address.deliver_pincode) + " " + deliver_address.deliver_type
                    transaction_id = 0
                    payment_mode = "COD"
                    payment_status = "Pending"
                    Delivery_expected = datetime.datetime.today() + datetime.timedelta(days=5)
                    if counter == 0:
                        cur_dt = datetime.datetime.now()
                    order_date_time = cur_dt

                    order = Order.objects.create(user=user, ordered_product=ordered_product, product_quantity=quantity, amount=amount,
                      email=email, address=address, payment_mode=payment_mode,
                      payment_status=payment_status, Delivery_expected=Delivery_expected, order_date_time=order_date_time)
                    order.save()
                    i.delete()
                return render(request, 'message.html', {'message':"Order Placed Successfully", 'suggestion':"Thanks for Shopping with us 😃😃😃 continue Shopping", 'mestype':"success", 'type':"home" })
            else:
                product = Addtocart.objects.get(product=from_order)
                user=request.user
                ordered_product = product.product
                quantity = product.quantity
                amount = product.product.products_selling_price * product.quantity
                email = request.user.email
                address = deliver_address.deliver_name + " " + str(deliver_address.deliver_mobile_no) + " " + deliver_address.deliver_locality + " " + deliver_address.deliver_address + " " + deliver_address.deliver_city + " " + deliver_address.deliver_state + " " + deliver_address.deliver_landmark + " " + str(deliver_address.deliver_pincode) + " " + deliver_address.deliver_type
                payment_mode = "COD"
                payment_status = "Pending"
                Delivery_expected = datetime.datetime.today() + datetime.timedelta(days=5)
                order_date_time = datetime.datetime.now()

                order = Order.objects.create(user=user, ordered_product=ordered_product,  product_quantity=quantity, amount=amount,
                      email=email, address=address, payment_mode=payment_mode,
                      payment_status=payment_status, Delivery_expected=Delivery_expected, order_date_time=order_date_time)
                order.save()
                product.delete()
                return render(request, 'message.html', {'message': 'Order Placed successfully', 'type': 'home', 'mestype': 'success', 'suggestion': 'Thanks for Shopping with us 😃😃😃! Continue for Shopping'})    
        else:
            # print('its a online payment')
            if from_order == 'addtocart':
                cart_amount = 0
                email=""
                cart_product = Addtocart.objects.filter(user_id=request.user)
                for i in cart_product:
                   cart_amount += i.total 
                razor = ""
                for counter, i in enumerate(cart_product):
                    user = request.user
                    ordered_product = i.product
                    quantity = i.quantity
                    amount = i.product.products_selling_price * i.quantity
                    email = request.user.email
                    address = deliver_address.deliver_name + " " + str(deliver_address.deliver_mobile_no) + " " + deliver_address.deliver_locality + " " + deliver_address.deliver_address + " " + deliver_address.deliver_city + " " + deliver_address.deliver_state + " " + deliver_address.deliver_landmark + " " + str(deliver_address.deliver_pincode) + " " + deliver_address.deliver_type
                    payment_mode = "Online Payment"
                    
                    order = Order.objects.create(user=user, ordered_product=ordered_product, product_quantity=quantity, amount=amount,
                      email=email, address=address, payment_mode=payment_mode)
                    order.save()
                    if counter == 0:
                        remove_comma = str(cart_amount).replace(",", "")
                        total_amount = int(float(str(remove_comma)[1:]))
                        order_currency = 'INR'
                        callback_url = 'http://127.0.0.1:8000/handlerequest/addtocart/'
                        notes = {'order-type': "basic order from the website", 'key':'value'}
                        razorpay_order = razorpay_client.order.create(dict(amount=total_amount*100, currency=order_currency, notes = notes, receipt=str(order.order_id), payment_capture='0'))
                        razor = razorpay_order['id']
                    order.razpory_order_id = razor
                    order.save()
                    i.delete()
                return render(request, 'confirmpayment.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'final_price':amount, 'razorpay_merchant_id':razorpay_id, 'callback_url':callback_url})

            else:
                product = Addtocart.objects.get(product=from_order, user_id=request.user)
                user=request.user
                ordered_product = product.product
                quantity = product.quantity
                amount = product.product.products_selling_price * product.quantity
                email = request.user.email
                address = deliver_address.deliver_name + " " + str(deliver_address.deliver_mobile_no) + " " + deliver_address.deliver_locality + " " + deliver_address.deliver_address + " " + deliver_address.deliver_city + " " + deliver_address.deliver_state + " " + deliver_address.deliver_landmark + " " + str(deliver_address.deliver_pincode) + " " + deliver_address.deliver_type
                payment_mode = "Online Payment"
                payment_status = "Pending"

                order = Order.objects.create(user=user, ordered_product=ordered_product,  product_quantity=quantity, amount=amount,
                      email=email, address=address, payment_mode=payment_mode,
                      payment_status=payment_status)
                order.save()
                product.delete()
                remove_comma = str(amount).replace(",", "")
                total_amount = int(float(str(remove_comma)[1:]))
                order_currency = 'INR'
                callback_url = 'http://127.0.0.1:8000/handlerequest/buy/'
                notes = {'order-type': "basic order from the website", 'key':'value'}
                razorpay_order = razorpay_client.order.create(dict(amount=total_amount*100, currency=order_currency, notes = notes, receipt=str(order.order_id), payment_capture='0'))
                order.razpory_order_id = razorpay_order['id']
                order.save()

                return render(request, 'confirmpayment.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'final_price':amount, 'razorpay_merchant_id':razorpay_id, 'callback_url':callback_url})
                  
    return redirect('home')

@csrf_exempt
def Handlerequest(request, order_type):
    if request.method == 'POST':
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': order_id, 
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature  
            }
            try:
                if order_type == 'addtocart':
                    order = Order.objects.filter(razpory_order_id=order_id)
                else:    
                    order = Order.objects.get(razpory_order_id=order_id)
            except:
                return HttpResponse('Not Found')
            if order_type == 'addtocart':
                amount=0
                for i in order:
                    i.razpory_payment_id=payment_id
                    i.razpory_signature_id=signature
                    i.save()
                    amount += i.amount
                result = razorpay_client.utility.verify_payment_signature(params_dict)
                if result:
                    remove_comma = str(amount).replace(",", "")
                    total_amount = int(float(str(remove_comma)[1:]))
                    amount = total_amount*100
                   
                    try:
                        razorpay_client.payment.capture(payment_id, amount)
                        for counter, i in enumerate(order):
                            i.payment_status = "Success"
                            i.order_status = "Your Order is Confirmed"
                            i.delivery_decription = "Delivery Expected On"
                            i.Delivery_expected = datetime.datetime.today() + datetime.timedelta(days=5)
                            if counter == 0:
                                cur_dt = datetime.datetime.now()
                            i.order_date_time = cur_dt
                            i.save()

                        return render(request, 'message.html', {'message': 'Order Placed successfully', 'type': 'home', 'mestype': 'success', 'suggestion': 'Thanks for Shopping with us 😃😃😃! Continue for Shopping'})
                    except:
                        for i in order:
                            i.payment_status = "Fail"
                            i.order_status = "Your Payment is Failed! Please try again"
                            i.delivery_decription = "Payment is not yet been done!!"
                            i.save()
                        return render(request, 'message.html', {'message': "Payment is Fail", 'type': 'home', 'mestype': 'error', 'suggestion': 'Payment is Failed please try again if your amount is deducted it will refund within 8-10 working days'})
                else:
                    for i in order:
                        i.payment_status = "Fail"
                        i.order_status = "Your Payment is Failed! Please try again"
                        i.delivery_decription = "Payment is not yet been done!!"
                        i.save()
                    return render(request, 'message.html', {'message': "Payment Fail", 'type': 'home', 'mestype': 'error', 'suggestion': 'Payment is Failed please try again if your amount is deducted it will refund within 8-10 working days'})
            else:
                order.razpory_payment_id=payment_id
                order.razpory_signature_id=signature
                order.save()
                result = razorpay_client.utility.verify_payment_signature(params_dict)
                if result:
                    remove_comma = str(order.amount).replace(",", "")
                    total_amount = int(float(str(remove_comma)[1:]))
                    amount = total_amount*100
                    print(amount)
                
                    try:
                        razorpay_client.payment.capture(payment_id, amount)
                        order.payment_status = "Success"
                        order.order_status = "Your Order is Confirmed"
                        order.delivery_decription = "Delivery Expected On"
                        order.Delivery_expected = datetime.datetime.today() + datetime.timedelta(days=5)
                        
                        order.order_date_time = datetime.datetime.now()
                        order.save()
                        return render(request, 'message.html', {'message': 'Order Placed successfully', 'type': 'home', 'mestype': 'success', 'suggestion': 'Thanks for Shopping with us 😃😃😃! Continue for Shopping'})
                    except:
                        order.payment_status = "Fail"
                        order.order_status = "Your Payment is Failed! Please try again"
                        order.delivery_decription = "Payment is not yet been done!!"
                        order.save()
                        return render(request, 'message.html', {'message': "Payment is Fail", 'type': 'home', 'mestype': 'error', 'suggestion': 'Payment is Failed please try again if your amount is deducted it will refund within 8-10 working days'})
                else:
                    order.payment_status = "Fail"
                    order.order_status = "Your Payment is Failed! Please try again"
                    order.delivery_decription = "Payment is not yet been done!!"
                    order.save()
                    return render(request, 'message.html', {'message': "Payment Fail", 'type': 'home', 'mestype': 'error', 'suggestion': 'Payment is Failed please try again if your amount is deducted it will refund within 8-10 working days'})

@login_required(login_url='login')
def MyOrders(request):
    if request.user.is_authenticated:
        user_avater = Profile.objects.get(user=request.user)
        orders = Order.objects.filter(user=request.user)
    else:
        user_avater=None
        orders = None

    cart_products = Addtocart.objects.filter(user_id=request.user)
    no_of_carts = cart_products.count()

    context = {
        'link':'order',
        'user_avater':user_avater,
        'no_of_carts':no_of_carts,
        'orders':orders,
    }
    return render(request, 'orders.html', context)

@login_required(login_url='login')
def OrderInformation(request, oid):
    orderdetail = Order.objects.get(order_id=oid)
    if request.user.is_authenticated:
        user_avater = Profile.objects.get(user=request.user)
        orders = Order.objects.filter(user=request.user)
    else:
        user_avater=None
        orders = None

    cart_products = Addtocart.objects.filter(user_id=request.user)
    no_of_carts = cart_products.count()

    ot = orderdetail.payment_mode
    if ot == 'COD':
        other_orders = Order.objects.filter(order_date_time=orderdetail.order_date_time, user=request.user).exclude(order_id=oid)
        print(orderdetail.order_date_time)
    else:
        other_orders = Order.objects.filter(razpory_order_id=orderdetail.razpory_order_id, user=request.user).exclude(order_id=oid)

    context = {
        'link':'order',
        'user_avater':user_avater,
        'no_of_carts':no_of_carts,
        'orderdetail':orderdetail,
        'other_order':other_orders,
    }
    return render(request, 'orderdetail.html', context)

@login_required(login_url='login')
def ContactUs(request):
    if request.user.is_authenticated:
        user_avater = Profile.objects.get(user=request.user)
    else:
        user_avater=None
        orders = None

    cart_products = Addtocart.objects.filter(user_id=request.user)
    no_of_carts = cart_products.count()

    context = {
        'link':'contact',
        'user_avater':user_avater,
        'no_of_carts':no_of_carts,
    }
    return render(request, 'contactus.html', context)

@login_required(login_url='login')
def AboutUs(request):
    if request.user.is_authenticated:
        user_avater = Profile.objects.get(user=request.user)
    else:
        user_avater=None
        orders = None

    cart_products = Addtocart.objects.filter(user_id=request.user)
    no_of_carts = cart_products.count()

    context = {
        'link':'about',
        'user_avater':user_avater,
        'no_of_carts':no_of_carts,
    }
    return render(request, 'aboutus.html', context)

@login_required(login_url='login')
def AddtoWishlist(request, pid):
    products = product.objects.get(products_id=pid)
    wishlists = Wishlist.objects.filter(product=products, user=request.user)

    if wishlists.exists():
        wishlists.delete()
        messages.success(request, "Removed from your wishlist")
        return redirect(request.META['HTTP_REFERER'])
    else:
        user = request.user
        wish_product = products

        wishlist = Wishlist.objects.create(user=user, product=wish_product)
        wishlist.save()
        messages.success(request, "Added to your wishlist")
        return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def DisplayWishlist(request):
    if request.user.is_authenticated:
        user_avater = Profile.objects.get(user=request.user)
        display_wish = Wishlist.objects.filter(user=request.user)
        dispaly_count = display_wish.count()
    else:
        user_avater=None
        orders = None

    cart_products = Addtocart.objects.filter(user_id=request.user)
    no_of_carts = cart_products.count()

    context = {
        'user_avater':user_avater,
        'no_of_carts':no_of_carts,
        'display_wish':display_wish,
        'dispaly_count':dispaly_count,
    }
    return render(request, 'wishlist.html', context)

@login_required(login_url='login')
def MyProfile(request):
    if request.user.is_authenticated:
        user_avater = Profile.objects.get(user=request.user)
    else:
        user_avater=None
    try:
        cart_products = Addtocart.objects.filter(user_id=request.user)
        address = DeliverAddress.objects.filter(user=request.user)
        no_of_carts = cart_products.count()
    except:
        cart_products = None
        no_of_carts = 0

    context = {
        'user_avater':user_avater,
        'no_of_carts':no_of_carts,
        'address':address,
    }
    return render(request, 'myprofile.html', context)

@login_required(login_url='login')
def UpdateProfile(request):
    if request.method == 'POST':
        if request.FILES:
            user_avater = request.FILES['img']
        else:
            user_profile = Profile.objects.get(user=request.user)
            user_avater = user_profile.user_avatar
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile')
        gender = request.POST.get('Gender')

        user = User.objects.get(username=request.user.username)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        user.save()

        user_profile = Profile.objects.get(user=request.user)
        user_profile.user_avatar = user_avater
        if mobile_no:
            user_profile.mobile_no = mobile_no
        if gender:
            user_profile.gender = gender
        user_profile.save()
        messages.success(request, "Your Profile updated successfully")
        return redirect(request.META['HTTP_REFERER'])

def Getsuggest(request):
    search_suggest = product.objects.all().values_list('products_name', flat=True)
    search = list(search_suggest)
    return JsonResponse(search, safe=False)

def searchMatch(search, item):
    if search in item.products_name or search in item.products_title.lower() or search in item.product_description.lower() or search in item.category_id.category_name.lower() or search in item.sub_category_id.sub_category_name.lower() or search in item.brand_id.brands_name.lower() or search in item.main_category_id.main_category_name.lower():
        return True
    else:
        return False

def Searchproductpage(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_avater = Profile.objects.get(user=request.user)
        else:
            user_avater=None
        try:
            cart_products = Addtocart.objects.filter(user_id=request.user)
            no_of_carts = cart_products.count()
        except:
            cart_products = None
            no_of_carts = 0
        search = request.GET.get('q')
        products = product.objects.all()
        prod = [item for item in products if searchMatch(search, item)]
        if (len(prod) == 0):
            prod = None
            pro = "no search results found........"
        else:
            pro = ""
            for i in prod:
                if len(i.product_slug) < 30:
                    en_prod = encrypt(i.product_slug)
                    i.product_slug = en_prod
                    i.save() 

        context={
            'prod':prod,
            'search':search,
            'user_avater':user_avater,
            'no_of_carts':no_of_carts,
            'pro':pro,
        }
        return render(request, 'searchproductpage.html', context)
    return render(request, 'searchproductpage.html')

def Crt(request, cid):
    cid = decrypt(cid)
    prod = product.objects.filter(category_id=cid)
    cat = category.objects.get(category_id=cid)
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_avater = Profile.objects.get(user=request.user)
        else:
            user_avater=None
        try:
            cart_products = Addtocart.objects.filter(user_id=request.user)
            no_of_carts = cart_products.count()
        except:
            cart_products = None
            no_of_carts = 0
    context={
        'prod':prod,
        'cid':cat,
        'user_avater':user_avater,
        'no_of_carts':no_of_carts,
    }
    return render(request, 'searchproductpage.html', context)

@login_required(login_url='login')
def Complaints(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')

        complaint = Complaint.objects.create(first_name=first_name, last_name=last_name, email=email, mobile=mobile, message=message)
        complaint.save()
        messages.success(request, "Message sent success")
        return redirect(request.META['HTTP_REFERER'])

def sending_mail(msg, to_email):
    send_mail(
        "Verifying your email",
        "Your Verification code is " + str(msg),
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )

def VerifyOTP(request, en_email, en_otp, otptype):
    if request.method == 'POST':
        inp1 = request.POST.get('1')
        inp2 = request.POST.get('2')
        inp3 = request.POST.get('3')
        inp4 = request.POST.get('4')
        inp5 = request.POST.get('5')
        inp6 = request.POST.get('6')
        otps = str(inp1) + str(inp2) + str(inp3) + str(inp4) + str(inp5) + str(inp6)

        de_otp = decrypt(en_otp)

        if otps == de_otp:
            if otptype == 'password':
                return render(request, 'newpass.html', {'en_email':en_email})
            else:
                return render(request, 'message.html', {'message': 'Registered successfully', 'type': 'login', 'mestype': 'success', 'suggestion': 'Continue with login'})
        else:
            return render(request, 'message.html', {'message': 'You entered OTP is incorrect', 'type': 'otp', 'mestype': 'error', 'suggestion': 'Please try again'})
    else:
        return render(request, 'verifyotp.html')
    
def ForgotPassword(request):
    return render(request, 'forgotpassword.html')

def SendOTP(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        en_email = encrypt(email)
        otp = random.randint(100000, 999999)
        str_otp = str(otp)
        en_otp = encrypt(str_otp)
        sending_mail(otp, email)
        otptype = "password"
        return redirect('verifyotp', en_email, otptype, en_otp)

def NewPassword(request, en_email):
    if request.method == 'POST':
        de_email = decrypt(en_email)
        password = request.POST.get('password')
        user = User.objects.get(email=de_email)
        user.set_password(password)
        user.save()
        return redirect('login')

def Logout(request):
    logout(request)
    return redirect('home')
