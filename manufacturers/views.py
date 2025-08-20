from django.shortcuts import render
from products.models import categories
from .models import manufacturers, manufacturer_page
import math


view = 30


def manufacturer_view(request):

    manufacturer_categories = categories.objects.filter(manufacturer_categories__isnull=False).distinct()

    exist_countries = []
    for i in manufacturers.objects.all():
        if i.country not in exist_countries:
            exist_countries.append(i.country)

    amount = manufacturers.objects.all().count()
    pages_array = []
    pages = math.ceil(amount / view)
    for k in range(1, pages+1):
        pages_array.append(k)

    content = {
        'manufacturers': manufacturers.objects.all(),
        'countries': exist_countries,
        'categories': manufacturer_categories,
        'manufacturer_page': manufacturer_page.objects.first(),
        'pages_array': pages_array,
        'all_manufacturers': manufacturers.objects.all(),
        'page': 1,
        'limit': view,
        'manufacturer_styles': True,
    }

    return render(request, 'proivoditeli.html', content)