from django.contrib import admin
from site_content.models import Content, SiteSection


class ContentAdmin(admin.ModelAdmin):
    model = Content
    list_display = ["name", "description", "icon", "section"]


class SiteSectionAdmin(admin.ModelAdmin):
    model = SiteSection
    list_display = ["name"]


admin.site.register(Content, ContentAdmin)
admin.site.register(SiteSection, SiteSectionAdmin)
# Register your models here.
