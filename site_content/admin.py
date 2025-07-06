from django.contrib import admin
from django.utils.safestring import mark_safe
from ordered_model.admin import (
    OrderedModelAdmin,
    OrderedInlineModelAdminMixin,
    OrderedStackedInline,
)
from site_content.models import Content, SiteSection, News


class ContentAdminInline(OrderedStackedInline):
    model = Content
    fields = [
        "name",
        "description",
        "icon",
        "order",
        "show_more_button",
        "show_more_content",
        "move_up_down_links",
    ]
    readonly_fields = ["order", "move_up_down_links"]
    ordering = ["order"]
    extra = 0


@admin.register(SiteSection)
class SiteSectionAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    inlines = [ContentAdminInline]
    model = SiteSection
    list_display = [
        "key",
        "name",
        "photo_list_preview",
        "_description",
        "move_up_down_links",
    ]
    ordering = ["order"]

    @admin.display(description="Photo")
    def photo_list_preview(self, obj):
        if obj.photo:
            return mark_safe(
                '<img src="{}" width="50" height="50" />'.format(obj.photo.url)
            )
        return ""

    def _description(self, obj):
        return mark_safe(obj.description)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    model = News
    list_display = ["date", "description"]


# Register your models here.
