from django.contrib import admin
from ordered_model.admin import OrderedInlineModelAdminMixin, OrderedStackedInline
from site_content.models import Content, SiteSection


class ContentAdminInline(OrderedStackedInline):
    model = Content
    fields = ["name", "description", "icon", 'order', 'move_up_down_links']
    readonly_fields = ["order", "move_up_down_links"]
    ordering = ["order"]
    extra = 0


class SiteSectionAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    inlines = [ContentAdminInline]
    model = SiteSection
    list_display = ["name"]


admin.site.register(SiteSection, SiteSectionAdmin)
# Register your models here.
