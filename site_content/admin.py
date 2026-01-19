from django.contrib import admin
from django.utils.safestring import mark_safe
from ordered_model.admin import OrderedModelAdmin
from site_content.models import Content, SiteSection, News, ContentPlanning


class ContentPlanningInline(admin.StackedInline):
    """Inline for editing planning entries within Content admin."""

    model = ContentPlanning
    extra = 1
    fields = ["date", "section", "educator", "description"]
    ordering = ["date", "section"]
    autocomplete_fields = ["educator"]


@admin.register(SiteSection)
class SiteSectionAdmin(OrderedModelAdmin):
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


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """Standalone admin for Content with planning inline."""

    model = Content
    inlines = [ContentPlanningInline]
    list_display = ["name", "section", "order", "has_show_more", "has_planning"]
    list_filter = ["section"]
    search_fields = ["name", "description"]
    ordering = ["section__order", "order"]  # Group by section order, then content order

    @admin.display(description="Show More")
    def has_show_more(self, obj):
        """Show checkmark if content has show_more_content."""
        if obj.show_more_content and obj.show_more_content.strip():
            return mark_safe('<span style="color: green;">✓</span>')
        return ""

    @admin.display(description="Planning")
    def has_planning(self, obj):
        """Show checkmark if content has planning entries."""
        if obj.planning_entries.exists():
            return mark_safe('<span style="color: green;">✓</span>')
        return ""


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    model = News
    list_display = ["date", "description"]


# Register your models here.
