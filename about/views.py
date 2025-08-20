from django.shortcuts import render
from .models import about_page, about_rules, about_manufacturers, about_team, about_supplies
from manufacturers.models import manufacturers


def about_view(request):

    all_mans = manufacturers.objects.filter(show_about=True)

    content = {
        'about_page': about_page.objects.first(),
        'about_rules': about_rules.objects.first(),
        'about_manufacturers': about_manufacturers.objects.first(),
        'about_mans': all_mans,
        'about_team': about_team.objects.first(),
        'about_supplies': about_supplies.objects.first(),
        'about_styles': True,
    }

    return render(request, 'about.html', content)

