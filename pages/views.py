from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PagesForm
import webpage_backend_use
import cosine_similarity_calc
import sys
import re
from urllib.request import urlretrieve 
from requests.utils import requote_uri 
python_path = sys.executable
from os.path import abspath, dirname, join
from django.conf import settings
from django.conf.urls.static import static


def get_price(item, zip_code):
    output = webpage_backend_use.django_input(item, zip_code)
    merchant = output[0]
    price = output[1]
    url = output[2] 
    #print(merchant, price, url)
    return merchant, price, url

# Create your views here.
def homePageView(request):
    if request.method == "POST":
        filled_form = PagesForm(request.POST)
        if filled_form.is_valid():
            note = "Thank you! Your %s is  \
            loading!" %(filled_form.cleaned_data['item_name'],)
            new_form = PagesForm()
        return render(request, 'pages/home.html',{'pagesform':new_form,'note':note})
    
    else:
        form = PagesForm()
        return render(request,'pages/home.html',{'pagesform':form})    

def processView(request):
    context={}
    item = request.POST.get('item_name')
    zipcode = request.POST.get('zip_code')
    merchant, price, imgurl = get_price(item, zipcode)
    
    if merchant !='No Merchant':
        nei_items = cosine_similarity_calc.calc_cosim(item)
        if nei_items != []:
            for itm in nei_items:
                nei_merchant, nei_price, nei_imgurl = get_price(itm, zipcode)
                if nei_merchant != 'No Merchant':
                    break
            context['nei_price'] = nei_price
            context['nei_merchant'] = nei_merchant
            context['nei_img'] = nei_imgurl
            context['nei_item'] = itm
        else:
            context['recomm'] = 'no_recomm'
                                
    context['price'] = price
    context['merchant'] = merchant
    context['img'] = imgurl
    context['item'] = item

    return render(request, 'pages/process.html', context)   

