from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from .models import about_page, about_rules_items, about_rules, about_manufacturers, about_team_items, about_team, about_supplies, about_supplies_items


class about_rules_items_admin(SortableInlineAdminMixin, admin.StackedInline):
    model = about_rules_items
    ordering = ('order',)
    extra = 0


class about_rules_admin(admin.ModelAdmin):
    save_on_top = True
    inlines = [about_rules_items_admin]
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class about_manufacturers_admin(admin.ModelAdmin):
    save_on_top = True
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class about_team_items_admin(SortableInlineAdminMixin, admin.StackedInline):
    model = about_team_items
    ordering = ('order',)
    extra = 0
    exclude = ('image_png2x', 'image_png',)
    readonly_fields = ('display_image',)


class about_team_admin(admin.ModelAdmin):
    save_on_top = True
    inlines = [about_team_items_admin]
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class about_supplies_items_admin(SortableInlineAdminMixin, admin.StackedInline):
    model = about_supplies_items
    ordering = ('order',)
    extra = 0


class about_supplies_admin(admin.ModelAdmin):
    save_on_top = True
    inlines = [about_supplies_items_admin]
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class about_page_admin(admin.ModelAdmin):
    save_on_top = True
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(about_page, about_page_admin)
admin.site.register(about_rules, about_rules_admin)
admin.site.register(about_manufacturers, about_manufacturers_admin)
admin.site.register(about_team, about_team_admin)
admin.site.register(about_supplies, about_supplies_admin)
