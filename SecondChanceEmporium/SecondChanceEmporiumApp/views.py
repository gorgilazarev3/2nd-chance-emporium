import random

import django
from django.contrib.auth import authenticate
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.template import Template
from django.db.models.signals import post_save
from .models import *
from django.db.models import Q
# Create your views here.
def index(request):
    newest_products = Product.objects.order_by('-id')[:4]
    context = {"newest_products":newest_products}
    return render(request,"index.html",context=context)

def allproducts(request):
    all_products = Product.objects.all()
    banner = 'all'
    context = {"products":all_products,"banner":banner}
    return render(request,"products.html",context=context)

def sale(request):
    all_products = list(Product.objects.all())
    # change 3 to how many random items you want
    random_items = random.sample(all_products, 4)
    banner = 'sale'
    context = {"products":random_items,"banner":banner}
    return render(request,"products.html",context=context)

def newest(request):
    all_products = Product.objects.order_by('-id')
    banner = 'all'
    context = {"products":all_products,"banner":banner}
    return render(request,"products.html",context=context)

def collectibles(request):
    category = Category.objects.filter(category__iexact="КОЛЕКЦИОНЕРСКИ ПАРЧИЊА").first()
    all_products = Product.objects.filter(category=category)
    banner = 'collectibles'
    context = {"products":all_products,"banner":banner}
    return render(request,"products.html",context=context)

def clothes(request):
    category = Category.objects.filter(category__iexact="ОБЛЕКА").first()
    all_products = Product.objects.filter(category=category)
    banner = 'clothes'
    context = {"products":all_products,"banner":banner}
    return render(request,"products.html",context=context)

def furniture(request):
    category = Category.objects.filter(category__iexact="МЕБЕЛ").first()
    all_products = Product.objects.filter(category=category)
    banner = 'furniture'
    context = {"products":all_products,"banner":banner}
    return render(request,"products.html",context=context)

def shoes(request):
    category = Category.objects.filter(category__iexact="ОБУВКИ").first()
    all_products = Product.objects.filter(category=category)
    banner = 'shoes'
    context = {"products":all_products,"banner":banner}
    return render(request,"products.html",context=context)

def miscellaneous(request):
    category = Category.objects.filter(category__iexact="РАЗНО").first()
    all_products = Product.objects.filter(category=category)
    banner = 'misc'
    context = {"products":all_products,"banner":banner}
    return render(request,"products.html",context=context)

def login(request):
    if request.method == 'POST':
        form_data = request.POST
        email = form_data.get("email_input")
        password = form_data.get("password_input")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            django.contrib.auth.login(request, user)
            return redirect('index')
        else:
            return redirect("login")
    return render(request,"login.html")

def register(request):
    if request.method == 'POST':
        form_data = request.POST
        name = form_data.get("name_input")
        email = form_data.get("email_input")
        password = form_data.get("password_input")
        is_seller = request.GET.get('seller', 'no')
        is_seller = True if is_seller == 'yes' else False
        shop_user = ShopUser(name=name,email=email,is_seller=is_seller)
        shop_user.password = password
        post_save.send(ShopUser, instance=shop_user, created=True)
        return redirect("login")

    is_seller = request.GET.get('seller', 'no')
    context = {"seller":is_seller}
    return render(request,"register.html",context)

def details(request, id):
    product = Product.objects.filter(id=id).first()
    stars = []
    for rating in range(0,int(product.seller.rating)):
        stars.append("star_fill")

    for rating in range(0, 5-len(stars)):
        stars.append("star_empty")

    num_ratings = random.randint(1,100)
    positive_percentage = float((num_ratings*product.seller.rating)/(num_ratings*5))*100

    similar_products = Product.objects.filter(category=product.category).filter(~Q(id=product.id))[:4]

    context = {"product":product, "num_ratings": num_ratings, "stars": stars, "percentage": positive_percentage, "similar_products": similar_products}
    return render(request,"details.html",context)


def addtocart(request):
    if request.method == 'POST':
        form_data = request.POST
        product_id = form_data.get("product_id")
        if request.user:
            shop_user = ShopUser.objects.filter(user_id=request.user).first()
            shopping_cart = ShoppingCart.objects.filter(user=shop_user).first()
            if not shopping_cart:
                shopping_cart = ShoppingCart(user=shop_user)
                shopping_cart.save()

            product = Product.objects.filter(id=product_id).first()
            product_in_cart = shopping_cart.products.filter(id=product_id)
            if not product_in_cart:
                shopping_cart.products.add(product)
            return redirect("details",product_id)

def cart(request):
    if request.user:
        shop_user = ShopUser.objects.filter(user_id=request.user).first()
        shopping_cart = ShoppingCart.objects.filter(user=shop_user).first()
        if not shopping_cart:
            shopping_cart = ShoppingCart(user=shop_user)
            shopping_cart.save()

        context = {"shopping_cart":shopping_cart,"products":shopping_cart.products.all()}
        return render(request,"shopping-cart.html",context)

def removefromcart(request):
    if request.user:
        product_id = request.GET.get('product_id', '-1')
        shop_user = ShopUser.objects.filter(user_id=request.user).first()
        shopping_cart = ShoppingCart.objects.filter(user=shop_user).first()
        product_in_cart = shopping_cart.products.filter(id=product_id).first()
        if product_in_cart:
            shopping_cart.products.remove(product_in_cart)
        return redirect("cart")

@receiver(post_save,sender=ShopUser)
def create_user(sender, instance, created, **kwargs):
    if created and instance:
        user = User.objects.filter(username=instance.email).first()
        if not user:
            user = User.objects.create_user(username=instance.email,
                                        email=instance.email,
                                        password=instance.password)
        instance.user_id = user
        instance.save()