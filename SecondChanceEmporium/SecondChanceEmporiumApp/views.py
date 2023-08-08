import random
import time
import django
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.template import Template
from django.db.models.signals import post_save
from .models import *
from django.db.models import Q
from django.core.mail import send_mail
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

def logout(request):
    if request.user.is_authenticated:
        django.contrib.auth.logout(request)
        return redirect("index")

def manageuser(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            shop_user = ShopUser.objects.filter(user_id=request.user).first()
            context = {"user":shop_user}
            return render(request,"user-management.html",context)
        elif request.method == "POST":
            form_data = request.POST
            name = form_data.get('user_name')
            username = form_data.get('user_email')
            shop_user = ShopUser.objects.filter(user_id=request.user).first()
            shop_user.name = name
            user = User.objects.filter(username=shop_user.email).first()
            shop_user.email = username
            user.username = username
            shop_user.save()
            user.save()
            return redirect("dashboard")

def changepassword(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form_data = request.POST
            oldpassword = form_data.get('user_oldpassword')
            newpassword = form_data.get('user_newpassword')
            confirmpassword = form_data.get('user_confirmpassword')
            username = form_data.get('user_email')
            user = authenticate(username=username, password=oldpassword)
            if user:
                if newpassword == confirmpassword:
                    user.set_password(newpassword)
                    user.save()
            return redirect("dashboard")
    return render(request,"change-password.html")



def register(request):
    if request.method == 'POST':
        form_data = request.POST
        name = form_data.get("name_input")
        email = form_data.get("email_input")
        password = form_data.get("password_input")
        is_seller = request.GET.get('seller', 'no')
        is_seller = True if is_seller == 'yes' else False
        rating = random.randint(1, 5)
        shop_user = ShopUser(name=name,email=email,is_seller=is_seller,rating=rating)
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
        if request.user.is_authenticated:
            shop_user = ShopUser.objects.filter(user_id=request.user).first()
            shopping_cart = ShoppingCart.objects.filter(user=shop_user).first()
            if not shopping_cart:
                shopping_cart = ShoppingCart(user=shop_user)
                shopping_cart.save()

            product = Product.objects.filter(id=product_id).first()
            product_in_cart = shopping_cart.products.filter(id=product_id)
            if not product_in_cart:
                shopping_cart.products.add(product)
                shopping_cart.total_price = shopping_cart.total_price + product.price
                shopping_cart.save()
            return redirect("details",product_id)
        return redirect("login")

def cart(request):
    if request.user.is_authenticated:
        shop_user = ShopUser.objects.filter(user_id=request.user).first()
        shopping_cart = ShoppingCart.objects.filter(user=shop_user).first()
        if not shopping_cart:
            shopping_cart = ShoppingCart(user=shop_user)
            shopping_cart.save()

        payment = request.GET.get('payment')
        context = {"shopping_cart":shopping_cart,"products":shopping_cart.products.all(),"payment":payment}
        return render(request,"shopping-cart.html",context)
    return redirect("login")

def removefromcart(request):
    if request.user.is_authenticated:
        product_id = request.GET.get('product_id', '-1')
        shop_user = ShopUser.objects.filter(user_id=request.user).first()
        shopping_cart = ShoppingCart.objects.filter(user=shop_user).first()
        product_in_cart = shopping_cart.products.filter(id=product_id).first()
        if product_in_cart:
            shopping_cart.products.remove(product_in_cart)
            shopping_cart.total_price = shopping_cart.total_price-product_in_cart.price
            shopping_cart.save()
        return redirect("cart")
    return redirect("login")


def order(request):
    if request.user.is_authenticated:
        shop_user = ShopUser.objects.filter(user_id=request.user).first()
        shopping_cart = ShoppingCart.objects.filter(user=shop_user).first()
        if shopping_cart.total_price > 0:
            all_products = shopping_cart.products.all()
            products_in_order = []
            products_in_order_ids = []
            for product in all_products:
                product_in_order = ProductInOrder.objects.filter(title=product.title).first()
                if not product_in_order:
                    product_in_order = ProductInOrder(title=product.title, category=product.category, description=product.description, cover_image=product.cover_image, price=product.price)
                    product_in_order.save()
                products_in_order.append(product_in_order)
                products_in_order_ids.append(product_in_order.id)
            order = Order(buyer=shop_user, total_price=shopping_cart.total_price)
            order.save()
            order.products.set(products_in_order_ids)
            shopping_cart.total_price = 0.0
            shopping_cart.products.clear()
            shopping_cart.save()
            context = {"products": products_in_order, "order": order}
            return render(request,"successful-order.html",context)

    return redirect("login")

def orderhistory(request):
    if request.user.is_authenticated:
        shop_user = ShopUser.objects.filter(user_id=request.user).first()
        orders = Order.objects.filter(buyer=shop_user)
        context = {"orders":orders}
        return render(request,"order-history.html",context)

def orderdetails(request, order_id):
    if request.user.is_authenticated:
        shop_user = ShopUser.objects.filter(user_id=request.user).first()
        order_obj = Order.objects.filter(id=order_id,buyer=shop_user).first()
        context = {"order":order_obj}
        return render(request,"order-details.html",context)

def dashboard(request):
    if request.user.is_authenticated:
        shop_user = ShopUser.objects.filter(user_id=request.user).first()
        context = {"user":shop_user}
        return render(request,"user-dashboard.html",context)
    return redirect("login")

def becomeseller(request):
    if request.user.is_authenticated:
        shop_user = ShopUser.objects.filter(user_id=request.user).first()
        shop_user.is_seller = True
        shop_user.save()
        context = {"user": shop_user}
        return render(request,"user-dashboard.html",context)
    return redirect("login")

def postnewproduct(request):
    if request.user.is_authenticated:
        shop_user = ShopUser.objects.filter(user_id=request.user).first()
        if request.method == 'GET':
            if shop_user.is_seller:
                categories = Category.objects.all()
                context = {"categories":categories}
                return render(request,"post-new-product.html",context)
        elif request.method == 'POST':
            if shop_user.is_seller:
                form_data = request.POST
                title = form_data.get('product_title')
                desc = form_data.get('product_description')
                category = form_data.get('product_category')
                category_obj = Category.objects.filter(id=category).first()
                images = request.FILES.getlist('product_images')
                cover_image = request.FILES.get("product_cover_image")
                price = form_data.get("product_price")
                if cover_image:
                    new_product = Product(title=title,description=desc,category=category_obj,cover_image=cover_image,is_approved=True,price=price,seller=shop_user)
                    new_product.save()
                else:
                    new_product = Product(title=title,description=desc,category=category_obj,cover_image=images[0],is_approved=True,price=price,seller=shop_user)
                    new_product.save()
                images_ids = []
                for image in images:
                    image_obj = ProductImage.objects.create(image=image)
                    images_ids.append(image_obj.id)
                new_product.images.set(images_ids)
                # message = ""
                # message = message.join("Здраво " + shop_user.name + "\n")
                # message = message.join(
                #     "Би сакале да Ве известиме дека вашиот оглас беше прегледан и ги исполнува барањата и соодветствува во целост со состојбата прикажана на фотографиите.\n")
                # message = message.join("Во прилог се деталите за вашиот успешно објавен оглас.\n")
                # message = message.join("Наслов: " + new_product.title + "\n")
                # message = message.join("Категорија: " + new_product.category.category + "\n")
                # message = message.join("Цена: " + new_product.price + "\n")
                # message = message.join("Ви благодариме за вашата соработка, 2ndChanceEmporium")
                # send_mail(
                #     "Известување за поставен оглас - 2ndChanceEmporium",
                #     message,
                #     "noreply@2ndchanceemporium.com",
                #     [shop_user.email],
                #     fail_silently=False,
                # )
                return render(request, "posted-product.html")
    return redirect("dashboard")

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