from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from astra.config import site_name, admin_url
from manufacturers.models import man_categories
from products.models import categories, catalog_page, subcategories, product
from .models import main_page
from main.forms import form_contact
from astra.sendform import send_excursion

from django.views.decorators.csrf import csrf_exempt


def main_view(request):
    content = {
        'main_page': main_page.objects.first(),
        'categories': categories.objects.all(),
        'catalog_page': catalog_page.objects.first(),
        'man_categories': man_categories.objects.all(),
        'main_styles': True,
    }

    return render(request, 'index.html', content)


def handle404(request, exception):
    return render(request, '404.html')


@csrf_exempt
def form_view(request):
    if request.method == 'POST':
        form = form_contact(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            company = form.cleaned_data['company']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            url = site_name + form.cleaned_data['url']
            file = request.FILES.get('file0')

            return send_excursion(name, company, phone, email, message, file, url)
    return HttpResponseNotFound("")


def robots_view(request):

    content = {
        'admin_url': admin_url,
        'site_name': site_name,
    }

    return render(request, 'robots.txt', content, content_type='text/plain')


def sitemap_view(request):

    content = {
        'site_name': site_name,
        'categories': categories.objects.all(),
        'subcategories': subcategories.objects.all(),
        'product': product.objects.all(),
    }

    return render(request, 'sitemap.xml', content, content_type='text/xml')
