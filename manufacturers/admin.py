from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from django.utils.html import format_html
from import_export.widgets import ForeignKeyWidget
from products.models import categories as Cats
from .models import country as Country, manufacturers, manufacturer_page, man_categories
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin


class manufacturers_admin(SortableAdminMixin, admin.ModelAdmin):
    model = manufacturers
    save_on_top = True
    ordering = ('order', 'name')
    readonly_fields = ('display_image',)
    exclude = ('image_png2x', 'image_png', 'image_about',)

    def get_categories(self, instance):
        return [categories.cat_title for categories in instance.categories.all()]
    get_categories.short_description = 'Категории'

    list_display = ['name', 'country', 'get_categories', 'man_categories', 'image_tag',]


class country_admin(admin.ModelAdmin):
    save_on_top = True


class man_categories_admin(admin.ModelAdmin):
    save_on_top = True


class manufacturer_page_admin(admin.ModelAdmin):
    save_on_top = True
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Country, country_admin)
admin.site.register(man_categories, man_categories_admin)
admin.site.register(manufacturer_page, manufacturer_page_admin)
admin.site.register(manufacturers, manufacturers_admin)
