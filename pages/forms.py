from django import forms

class PagesForm(forms.Form):
    item_name = forms.CharField(label = 'Item Name', max_length = 120)
    zip_code = forms.CharField(label = 'Zip Code', max_length= 6)