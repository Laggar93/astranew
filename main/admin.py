from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from .models import main_page, main_page_items


class main_page_items_admin(SortableInlineAdminMixin, admin.StackedInline):
    model = main_page_items
    ordering = ('order',)
    extra = 0


class main_page_admin(admin.ModelAdmin):
    save_on_top = True
    inlines = [main_page_items_admin]
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(main_page, main_page_admin)
