from django.urls import path
from . import views


urlpatterns = [
    path('catalogue/', views.catalog_view, name='catalog'),
    path('catalogue/<str:cat_slug>/', views.category_view, name='category'),
    path('catalogue/<str:cat_slug>/<str:subcat_slug>/', views.subcategory_view, name='subcategory'),
    path('catalogue/<str:cat_slug>/<str:subcat_slug>/<str:product_slug>/', views.product_detail_view, name='product_detail'),
]