from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PagesForm
import subprocess
import sys
import re
from urllib.request import urlretrieve 
from requests.utils import requote_uri 
python_path = sys.executable
from os.path import abspath, dirname, join
 



def get_price(item, zip_code):
    output = subprocess.check_output([python_path, 'webpage_backend_use.py', item, zip_code], \
                shell=True).decode('utf-8')
    
    output1 = output.split(', ')
    merchant = output1[0].strip("(")
    price = output1[1].strip(" '' ")
    url1 = output1[2].replace(")","")
    url2 = url1.strip()
    url = url2. strip(" '' ")
    
    return merchant,price,url

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
    context['price'] = price
    context['merchant'] = merchant
    context['img'] = imgurl
    context['item'] = item

    return render(request, 'pages/process.html', context)   

