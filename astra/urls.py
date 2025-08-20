from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.urls import path
from main.views import handle404, form_view, robots_view, sitemap_view
from astra import settings


urlpatterns = [
    path('d4G7jd2N95h/', admin.site.urls),
    path('form/', form_view, name='form'),
    path('robots.txt', robots_view, name='robots_view'),
    path('sitemap.xml', sitemap_view, name='sitemap_view'),
    path('', include('about.urls')),
    path('', include('contacts.urls')),
    path('', include('main.urls')),
    path('', include('products.urls')),
    path('', include('manufacturers.urls')),
]


handler404=handle404


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)