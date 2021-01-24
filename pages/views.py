from django.shortcuts import render
from django.http import HttpResponse
from .forms import PagesForm
import subprocess as sp

# Create your views here.
def homePageView(request):
    if request.method == "POST":
        filled_form = PagesForm(request.POST)
        if filled_form.is_valid():
            note = "Thank you! Your %s is  \
            loading!" %(filled_form.cleaned_data['item_name'],)
            item_name = filled_form.cleaned_data['item_name']
            zip_code = filled_form.cleaned_data['zip_code']
            new_form = PagesForm()
            search_out = script_function(item_name, zip_code)
            return render(request, 'pages/home.html', \
                {'pagesform':new_form,'note':note,'search_out':search_out})
    
    else:
        form = PagesForm()
        return render(request,'pages/home.html',{'pagesform':form})    
    
def script_function(item_name,zip_code):
#   print(post_from_form)
     script_output = sp.check_output(['C:/Users/Ursa Major/Documents/Data_Science/Projects    \
                                  /SharpestMinds/Flipp_programs/webpage_backend_use.py'],   \
                             str(item_name),zip_code)
     return script_output
    