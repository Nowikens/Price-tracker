from django.shortcuts import render, redirect
from .models import Product

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
            
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'index/home.html', context)