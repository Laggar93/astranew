import re
from django import forms


class form_contact(forms.Form):
    name = forms.CharField(required=True)
    company = forms.CharField(required=True)
    phone = forms.RegexField(regex=r'^[\+\-\ \(\)0-9]+$', max_length=50, required=True)
    email = forms.RegexField(regex=re.compile(r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'))
    message = forms.CharField(required=True)
    file = forms.FileField(required=False)
    url = forms.CharField(required=True)
