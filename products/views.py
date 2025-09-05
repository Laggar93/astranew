from django.shortcuts import render, get_object_or_404
from itertools import zip_longest
from .models import catalog_page, categories, subcategories, product, brands, countries
from .forms import products_filter_form
import math


def catalog_view(request):

    content = {
        'catalog_page': catalog_page.objects.first(),
        'categories': categories.objects.all(),
        'is_new': True,
    }

    return render(request, 'catalog.html', content)


def category_view(request, cat_slug):
    current_category = get_object_or_404(categories, slug=cat_slug)

    content = {
        'current_category': current_category,
        'catalog_page': catalog_page.objects.first(),
    }

    return render(request, 'oborudovanie.html', content)


def subcategory_view(request, cat_slug, subcat_slug):
    current_category = get_object_or_404(categories, slug=cat_slug)
    current_subcategory = get_object_or_404(subcategories, slug=subcat_slug)
    all_mans = current_subcategory.manufacturers.all()

    content = {
        'current_category': current_category,
        'current_subcategory': current_subcategory,
        'products_leftovers': product.objects.filter(subcategories__slug=subcat_slug).filter(leftovers=True),
        'products_pop_models': product.objects.filter(subcategories__slug=subcat_slug).filter(pop_models=True),
        'catalog_page': catalog_page.objects.first(),
        'about_mans': list(zip_longest(all_mans[::2], all_mans[1::2])),
        'products_left': product.objects.filter(leftovers=True),
        'subcat_styles': True
    }

    return render(request, 'term-analiz.html', content)


def product_detail_view(request, cat_slug, subcat_slug, product_slug):
    current_category = get_object_or_404(categories, slug=cat_slug)
    current_subcategory = get_object_or_404(subcategories, slug=subcat_slug)
    current_product = get_object_or_404(product, slug=product_slug)

    content = {
        'current_category': current_category,
        'current_subcategory': current_subcategory,
        'current_product': current_product,
        'products_leftovers': product.objects.filter(subcategories__slug=subcat_slug).filter(leftovers=True),
        'products_pop_models': product.objects.filter(subcategories__slug=subcat_slug).filter(pop_models=True),
        'catalog_page': catalog_page.objects.first(),
    }

    return render(request, 'product-detail.html', content)


def replace_data(data, name, result):

    if name in data:
        k = str(data).split(name)[1][5:]
        k = k[0:k.find(']')-1].replace("', '", ',')
        result[name] = k

    return result


def filter_products(data, category, subcategory=None):

    mutable_querydict = data.copy()
    
    mutable_querydict = replace_data(data, 'brand', mutable_querydict)
    mutable_querydict = replace_data(data, 'country', mutable_querydict)
    mutable_querydict = replace_data(data, 'params', mutable_querydict)

    if subcategory:
        all_products = product.objects.filter(subcategories__categories=category, subcategories=subcategory)
    else:
        all_products = product.objects.filter(subcategories__categories=category)
    
    all_products_anyway = all_products

    filter = products_filter_form(mutable_querydict)

    search = None
    brand = None
    country = None
    price_from = None
    price_to = None
    params = None
    instock = None
    amount = None
    sort = None
    page = None

    if filter.is_valid():

        filter_cleaned = filter.cleaned_data
        search = filter_cleaned['search']
        brand = filter_cleaned['brand']
        country = filter_cleaned['country']
        price_from = filter_cleaned['price_from']
        price_to = filter_cleaned['price_to']
        params = filter_cleaned['params']
        instock = filter_cleaned['instock']
        amount = filter_cleaned['amount']
        sort = filter_cleaned['sort']
        page = filter_cleaned['page']
        
        if brand:
            brand = [int(part) for part in brand.split(',')]
            all_products = all_products.filter(brands__in=brand).distinct()
        
        if country:
            country = [int(part) for part in country.split(',')]
            all_products = all_products.filter(countries__in=country).distinct()
        
        if search:
            for k in all_products:
                if search.lower() not in k.product_title.lower():
                    all_products = all_products.exclude(id=k.id)
        
        if price_from:
            if price_to:
                if price_to >= price_from:
                    all_products = all_products.filter(product_price__lte=price_to)
            all_products = all_products.filter(product_price__gte=price_from)
        
        if params:
            params = [int(part) for part in params.split(',')]
            all_products = all_products.filter(filters__in=params).distinct()
        
        if instock:
            all_products = all_products.filter(instock=True)
        
        if sort == 'new':
            all_products = all_products.order_by('-id')
        
        if sort == 'price_asc':
            all_products = all_products.order_by('product_price')
        
        if sort == 'price_desc':
            all_products = all_products.order_by('-product_price')
    
    if page == None:
        page = 1
    
    if amount == None:
        amount = 36
    
    pages = math.ceil(all_products.count() / amount)

    if not sort or sort == 'name':
        all_products = all_products.order_by('product_title')
    
    all_products = all_products[0:page*amount]
    
    return all_products, [search, subcategory, brand, country, price_from, price_to, params, instock, amount, sort, page], pages, all_products_anyway


def products_view(request, cat_slug, subcat_slug=None):
    
    current_category = get_object_or_404(categories, slug=cat_slug)

    if subcat_slug:
        current_subcategory = get_object_or_404(subcategories, slug=subcat_slug, categories=current_category)
        current_page = current_subcategory
        current_brands = brands.objects.filter(product_brands__subcategories=current_subcategory).distinct()
        current_countries = countries.objects.filter(product_country__subcategories=current_subcategory).distinct()
    else:
        current_subcategory = None
        current_page = current_category
        current_brands = brands.objects.filter(product_brands__subcategories__categories=current_category).distinct()
        current_countries = countries.objects.filter(product_country__subcategories__categories=current_subcategory).distinct()
    
    current_subcategories = subcategories.objects.filter(categories=current_category).exclude(products_subcategory=None).order_by('subcategory_title')
    if subcat_slug:
        faq = current_page.faq_subcategories.all()
    else:
        faq = current_page.faq_categories.all()
    
    filter_results = filter_products(request.GET, current_category, current_subcategory)

    pages = filter_results[2]
    pages_array = list(range(1, pages+1))

    filters = {}
    products_all = filter_results[3]
    for k in products_all.order_by('filters__filters__filter_title'):
        for s in k.filters.all().order_by('filters__filter_title'):
            k = None
            try:
                k = filters[s.filters.filter_title]
            except:
                filters[s.filters.filter_title] = [s]
            if k:
                if not s in k:
                    k.append(s)
    
    page_val = filter_results[1][10]
    page_add = ''
    if page_val != 1:
        page_add = ' - страница ' + str(page_val)
        hide_seo_faq = True
    else:
        hide_seo_faq = False
    
    pars = {}
    
    for k in request.GET.items():
        if k[0] != 'page':
            pars[k[0]] = k[1].replace(',', '%2C')

    content = {
        'subcategories': current_subcategories,
        'is_filter': True,
        'current_category': current_category,
        'current_subcategory': current_subcategory,
        'page_title': current_page.title + page_add,
        'page_description': current_page.description + page_add,
        'page_keywords': current_page.keywords,
        'catalog_page_name': catalog_page.objects.first().section_title,
        'brands': current_brands,
        'countries': current_countries,
        'products': filter_results[0],
        'params': filter_results[1],
        'brand_len': len(filter_results[1][2]),
        'country_len': len(filter_results[1][3]),
        'pages': pages,
        'pages_array': pages_array,
        'seo': current_page.seo,
        'faq': faq,
        'filters': filters,
        'hide_seo_faq': hide_seo_faq,
        'pars': pars,
        'page_val': page_val,
    }

    return render(request, 'filter.html', content)


def products_ajax_view(request, cat_slug, subcat_slug=None):
    
    current_category = categories.objects.filter(slug=cat_slug).first()

    try:
        current_subcategory = subcategories.objects.filter(categories=current_category, slug=subcat_slug).first()
    except:
        current_subcategory = None
    
    filter_results = filter_products(request.POST, current_category, current_subcategory)

    pages = filter_results[2]
    pages_array = list(range(1, pages+1))
    
    pars = {}
    
    for k in request.POST.items():
        if k[0] != 'page' and k[1] != '' and k[0] != 'csrfmiddlewaretoken':
            pars[k[0]] = k[1].replace(',', '%2C')

    content = {
        'products': filter_results[0],
        'params': filter_results[1],
        'pages': pages,
        'pages_array': pages_array,
        'pars': pars,
        'current_subcategory': current_subcategory,
    }

    return render(request, 'ajax.html', content)


def products_item_view(request, cat_slug, subcat_slug, product_slug):

    current_category = get_object_or_404(categories, slug=cat_slug)
    current_subcategory = get_object_or_404(subcategories, categories=current_category, slug=subcat_slug)
    current_product = get_object_or_404(product, subcategories__categories=current_category, subcategories=current_subcategory, slug=product_slug)

    content = {
        'catalog_page': catalog_page.objects.first(),
        'current_category': current_category,
        'current_subcategory': current_subcategory,
        'current_product': current_product,
        'page_title': current_product.title,
        'page_description': current_product.description,
        'page_keywords': current_product.keywords,
        'seo': current_product.seo,
        'faq': current_subcategory.faq_subcategories.all(),
        'is_filter': True,
        'is_card': True,
        'similar_products': product.objects.filter(subcategories=current_subcategory).exclude(id=current_product.id).order_by('?')[:8]
    }

    return render(request, 'product.html', content)