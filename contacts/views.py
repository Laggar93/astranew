from django.shortcuts import render
from .models import contacts, requisites


def contacts_view(request):

    content = {
        'contacts_page': contacts.objects.first(),
        'requisites': requisites.objects.first(),
        'contact_styles': True,
    }

    return render(request, 'contacts.html', content)
