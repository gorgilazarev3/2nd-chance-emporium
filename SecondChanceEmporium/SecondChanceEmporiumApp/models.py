from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ShopUser(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=255,blank=False)
    email = models.EmailField()
    is_seller = models.BooleanField()
    rating = models.DecimalField(decimal_places=1,max_digits=2,default=0.0,blank=True)

    def __str__(self):
        return f"{self.user_id.username}"

class Category(models.Model):
    category = models.CharField(max_length=255,blank=False,null=False)

    def __str__(self):
        return f"{self.category}"


class ProductImage(models.Model):
    image = models.ImageField(upload_to="files/")

class Product(models.Model):
    title = models.CharField(max_length=255,blank=False,null=False)
    category = models.ForeignKey(to=Category,on_delete=models.CASCADE)
    description = models.CharField(max_length=255,blank=False,null=False)
    images = models.ManyToManyField(to=ProductImage,symmetrical=False,blank=True)
    cover_image = models.ImageField(upload_to="files/")
    is_approved = models.BooleanField()
    seller = models.ForeignKey(to=ShopUser,on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2,max_digits=10)

    def __str__(self):
        return f"{self.title} - {self.category} - {self.price}$"

class Order(models.Model):
    product = models.ForeignKey(to=Product,on_delete=models.CASCADE)
    buyer = models.ForeignKey(to=ShopUser,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.title} - {self.buyer.name} - {self.product.price}$"

