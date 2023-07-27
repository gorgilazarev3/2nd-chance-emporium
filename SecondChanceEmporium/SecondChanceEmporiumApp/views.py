from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    newest_products = Product.objects.all().reverse()[:4]
    context = {"newest_products":newest_products}
    return render(request,"index.html",context=context)