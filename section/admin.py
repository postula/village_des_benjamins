from django.contrib import admin
from section.models import Section
from ordered_model.admin import OrderedModelAdmin


@admin.register(Section)
class SectionAdmin(OrderedModelAdmin):
    model = Section
    list_display = ["name", "min_age", "max_age", "move_up_down_links"]
    ordering = ["order"]


# Register your models here.
