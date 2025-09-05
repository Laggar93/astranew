from contacts.models import contacts, requisites
from about.models import about_page
from products.models import catalog_page
from manufacturers.models import manufacturer_page
from main.models import main_page
from main.forms import form_contact
from astra.config import site_name


v = '?v=6'


def globals(request):

    context = {
        'contacts_page': contacts.objects.first(),
        'requisites': requisites.objects.first(),
        'about_page': about_page.objects.first(),
        'catalog_page': catalog_page.objects.first(),
        'main_page': main_page.objects.first(),
        'manufacturer_page': manufacturer_page.objects.first(),
        'form_contact': form_contact,
        'site_name': site_name,
        'v': v,
    }

    return context