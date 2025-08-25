from django import forms
import re


class products_filter_form(forms.Form):
    search = forms.CharField(required=False)
    subcategory = forms.RegexField(regex=r'^[0-9,]*$', required=False)
    brand = forms.RegexField(regex=r'^[0-9,]*$', required=False)
    country = forms.RegexField(regex=r'^[0-9,]*$', required=False)
    price_from = forms.IntegerField(required=False)
    price_to = forms.IntegerField(required=False)
    instock = forms.BooleanField(required=False)
    amount = forms.IntegerField(required=False)
    sort = forms.RegexField(regex=re.compile(r'\b(name|new|price_asc|price_desc)\b'), required=False)
    page = forms.IntegerField(required=False)