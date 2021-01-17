from django.contrib import admin
from ordered_model.admin import OrderedInlineModelAdminMixin, OrderedStackedInline
from site_content.models import Content, SiteSection, News


class ContentAdminInline(OrderedStackedInline):
    model = Content
    fields = ["name", "description", "icon", 'order',"show_more_button", "show_more_content", 'move_up_down_links']
    readonly_fields = ["order", "move_up_down_links"]
    ordering = ["order"]
    extra = 0


class SiteSectionAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    inlines = [ContentAdminInline]
    model = SiteSection
    list_display = ["key", "name", "description"]


class NewsAdmin(admin.ModelAdmin):
    model = News
    list_display = ["date", "description"]


admin.site.register(SiteSection, SiteSectionAdmin)
admin.site.register(News, NewsAdmin)
# Register your models here.
