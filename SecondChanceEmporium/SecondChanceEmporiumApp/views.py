import django
from django.contrib.auth import authenticate
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.template import Template
from django.db.models.signals import post_save
from .models import *
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