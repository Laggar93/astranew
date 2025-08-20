from django.shortcuts import render, get_object_or_404
from itertools import zip_longest
from .models import catalog_page, categories, subcategories, product


def catalog_view(request):

    content = {
        'catalog_page': catalog_page.objects.first(),
        'categories': categories.objects.all(),
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

