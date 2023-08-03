"""
URL configuration for SecondChanceEmporium project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from SecondChanceEmporiumApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('products/all',allproducts,name="allproducts"),
    path('products/newest',newest,name="newest"),
    path('products/clothes',clothes,name="clothes"),
    path('products/shoes',shoes,name="shoes"),
    path('products/misc',miscellaneous,name="miscellaneous"),
    path('products/furniture',furniture,name="furniture"),
    path('products/collectibles',collectibles,name="collectibles"),
    path('products/sale',sale,name="sale"),
    path('login/',login,name="login"),
    path('register/',register,name="register"),
    path('add-to-cart/',addtocart,name="addtocart"),
    path('remove-from-cart/',removefromcart,name="removefromcart"),
    path('cart/',cart,name="cart"),
    path('product/<int:id>',details,name="details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
