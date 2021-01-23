from django import forms

class PagesForm(forms.Form):
    item_name = forms.CharField(label = 'Item Name', max_length = 120)
    zip_code = forms.IntegerField(label = 'Zip Code')