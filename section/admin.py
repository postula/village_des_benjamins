from django.contrib import admin
from section.models import Section


class SectionAdmin(admin.ModelAdmin):
    model = Section
    list_display = ["name", "min_age", "max_age"]


admin.site.register(Section, SectionAdmin)

# Register your models here.
