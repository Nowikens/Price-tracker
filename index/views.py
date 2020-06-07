from django.shortcuts import render, redirect
from .models import Product
from accounts.models import UserProfile
import requests
from bs4 import BeautifulSoup

import datetime
import pytz
import re

# Create your views here.


def index(request):
    tz = pytz.timezone('Europe/Warsaw')
    warsaw_now = datetime.datetime.now(tz)
            
    URL = 'https://selectshop.pl/longboard-cruiser-komplety,40/0/price-asc'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser') 
    products_elements = soup.find_all(class_="product")
    
    for product_elem in products_elements:
        product_image = 'https://selectshop.pl/'+product_elem.find(class_='head').find('a').find('img')['src']
        
        product_name = product_elem.find('h2').text
        
        product_price = product_elem.find(class_='price')
        
        float_product_price = float(product_price.text.replace(',', '.').replace(" zł", ""))
        
        product_id = product_elem.find('h2').get('id')
        
        product_url = 'https://selectshop.pl/'+product_elem.find(class_='head').find('a').get('href')

        
        
        
        if not Product.objects.filter(shop_product_id=product_id).exists():

            new_product = Product.objects.create(
            
                name            = product_name, 
                image_url       = product_image,
                product_url     = product_url,
                price           = float_product_price, 
                shop_product_id = product_id,
                last_update     = warsaw_now,
                )

        else:
            updating_product = Product.objects.get(shop_product_id=product_id)
            updating_product.last_update = warsaw_now
            updating_product.save()
            
    
    user_products = []
    if request.user.is_authenticated:
        user_products = Product.objects.filter(userprofile=request.user.userprofile.id)
    
    
    
    products = Product.objects.all()
    context = {'products': products, 'user_products': user_products}
    return render(request, 'index/home.html', context)
    
def add_wanted_product(request, pk):
    product_to_add = Product.objects.get(pk=pk)
    user = UserProfile.objects.get(pk=request.user.userprofile.id)
    
    user.wanted_products.add(product_to_add)
    
    return redirect('index:home')


def remove_wanted_product(request, pk):
    product_to_remove = Product.objects.get(pk=pk)
    user = UserProfile.objects.get(pk=request.user.userprofile.id)
    
    user.wanted_products.remove(product_to_remove)
    
    return redirect('index:home')