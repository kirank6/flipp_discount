from django.shortcuts import render
from django.http import HttpResponse
from .forms import PagesForm
import subprocess 

# Create your views here.
def homePageView(request):
    if request.method == "POST":
        filled_form = PagesForm(request.POST)
        if filled_form.is_valid():
            note = "Thank you! Your %s is  \
            loading!" %(filled_form.cleaned_data['item_name'],)
            new_form = PagesForm()
            # script_function(filled_form)
            return render(request, 'pages/home.html',{'pagesform':new_form,'note':note})
    
    else:
        form = PagesForm()
        return render(request,'pages/home.html',{'pagesform':form})    
    
# def script_function(post_from_form):
#     print(post_from_form)
#     return subprocess.check_call(['C:/Users/Ursa Major/Documents/Data_Science/Projects  \
#                                   /SharpestMinds/Flipp_programs/webpage_backend_use.py'], post_from_form)
    