from django import forms

class PagesForm(forms.Form):
    item_name = forms.CharField(label = 'ITEM NAME', max_length = 120)
    zip_code = forms.CharField(label = 'ZIP CODE', max_length= 6)