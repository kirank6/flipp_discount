from django.shortcuts import render
from django.http import HttpResponse
from .forms import PagesForm

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