from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from contacts.models import contacts, requisites, requisites_items


class requisites_items_admin(SortableInlineAdminMixin, admin.StackedInline):
    model = requisites_items
    ordering = ('order',)
    extra = 0


class requisites_admin(admin.ModelAdmin):
    inlines = [requisites_items_admin]
    save_on_top = True
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class contacts_admin(admin.ModelAdmin):
    save_on_top = True
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(contacts, contacts_admin)
admin.site.register(requisites, requisites_admin)
