from django.contrib import admin, auth
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.html import format_html
admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from .models import catalog_page, categories, subcategories, product, product_parameters, product_chars, brands, countries, faq_catalogue_page, faq_categories, product_slider, product_file, filters, filters_parameters


class filters_parameters_admin(admin.StackedInline):
    model = filters_parameters
    extra = 0


class filters_admin(admin.ModelAdmin):
    save_on_top = True
    inlines = [filters_parameters_admin]


class faq_catalogue_page_admin(SortableInlineAdminMixin, admin.StackedInline):
    model = faq_catalogue_page
    ordering = ('order',)
    extra = 0


class faq_categories_admin(SortableInlineAdminMixin, admin.StackedInline):
    model = faq_categories
    ordering = ('order',)
    extra = 0


class subcategoriesAdminForm(forms.ModelForm):
    class Meta:
        model = subcategories
        fields = '__all__'
        widgets = {
            'manufacturers': FilteredSelectMultiple('Производители', is_stacked=False, attrs={'style': 'height: 300px; width: 400px;'}),
        }


class product_slider_admin(SortableInlineAdminMixin, admin.StackedInline):
    model = product_slider
    ordering = ('order',)
    readonly_fields = ('display_image',)
    extra = 0


class product_file_admin(SortableInlineAdminMixin, admin.StackedInline):
    model = product_file
    ordering = ('order',)
    extra = 0

class categories_admin(SortableAdminMixin, admin.ModelAdmin):
    model = categories
    save_on_top = True
    ordering = ('order',)
    readonly_fields = ('display_image',)
    inlines = [faq_categories_admin]
    exclude = ('image_2x_webp', 'image_2x_jpg', 'image_webp', 'image_jpg',)


class subcategories_admin(SortableAdminMixin, admin.ModelAdmin):
    model = subcategories
    save_on_top = True
    ordering = ('order',)
    readonly_fields = ('display_image', 'display_icon',)
    exclude = ('image_2x_webp', 'image_2x_jpg', 'image_webp', 'image_jpg',)
    list_display = ['subcategory_title', 'categories']
    form = subcategoriesAdminForm


class product_parameters_admin(SortableInlineAdminMixin, admin.StackedInline):
    model = product_parameters
    ordering = ('order',)
    extra = 0


class product_chars_admin(SortableInlineAdminMixin, admin.StackedInline):
    model = product_chars
    ordering = ('order',)
    extra = 0


class product_admin(SortableAdminMixin, admin.ModelAdmin):
    model = product
    inlines = [product_parameters_admin, product_chars_admin, product_slider_admin, product_file_admin]
    save_on_top = True
    ordering = ('order',)
    readonly_fields = ('display_image',)
    exclude = ('image_detail_png2x', 'image_detail_png', 'image_detail_webp',
               'image_other_png2x', 'image_other_png', 'image_other_webp',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" />'.format(obj.image.url))
    image_tag.short_description = 'Изображение'

    list_display = ['product_title', 'subcategories', 'image_tag', 'leftovers', 'pop_models',]


class subcategory_page_admin(admin.ModelAdmin):
    save_on_top = True
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class catalog_page_admin(admin.ModelAdmin):
    inlines = [faq_catalogue_page_admin]
    save_on_top = True
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class brands_admin(admin.ModelAdmin):
    ordering = ('-brand_title',)


class countries_admin(admin.ModelAdmin):
    ordering = ('-country_title',)


admin.site.register(catalog_page, catalog_page_admin)
admin.site.register(categories, categories_admin)
admin.site.register(subcategories, subcategories_admin)
admin.site.register(product, product_admin)
admin.site.register(brands, brands_admin)
admin.site.register(countries, countries_admin)
admin.site.register(filters, filters_admin)