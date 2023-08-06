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
from django.contrib.auth import views as auth_views

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
    path('logout/',logout,name="logout"),
    path('register/',register,name="register"),
    path('user-management/',manageuser,name="manageuser"),
    path('change-password/',changepassword,name="changepassword"),
    path('add-to-cart/',addtocart,name="addtocart"),
    path('remove-from-cart/',removefromcart,name="removefromcart"),
    path('cart/',cart,name="cart"),
    path('order/',order,name="order"),
    path('order-history/',orderhistory,name="orderhistory"),
    path('dashboard/',dashboard,name="dashboard"),
    path('become-seller/',becomeseller,name="becomeseller"),
    path('new-product/',postnewproduct,name="postnewproduct"),
    path('product/<int:id>',details,name="details"),
    path('order-details/<int:order_id>',orderdetails,name="orderdetails"),
path(
    "password_reset/",
    auth_views.PasswordResetView.as_view(),
    name="admin_password_reset",
),
path(
    "password_reset/done/",
    auth_views.PasswordResetDoneView.as_view(),
    name="password_reset_done",
),
path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(),
    name="password_reset_confirm",
),
path(
    "reset/done/",
    auth_views.PasswordResetCompleteView.as_view(),
    name="password_reset_complete",
),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
