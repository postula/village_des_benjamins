from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from holiday.models import Holiday, HolidaySection, Registration, Outing


class OutingInline(admin.StackedInline):
    model = Outing
    extra = 0


class HolidaySectionAdmin(admin.ModelAdmin):
    model = HolidaySection
    extra = 0
    inlines = [OutingInline]
    list_display = ["section", "holiday", "capacity", "remaining_capacity"]
    list_filter = ["section", "holiday", "capacity"]


# Register your models here.
class HolidayAdmin(admin.ModelAdmin):
    model = Holiday
    list_display = ["name", "start_date", "end_date", "price", "registration_open"]


class RegistrationAdmin(admin.ModelAdmin, DynamicArrayMixin):
    model = Registration
    list_display = ["holiday", "child", "number_of_days", "status", "cost"]
    list_filter = [
        "holiday",
        "child__parent",
        "status",
    ]


admin.site.register(Holiday, HolidayAdmin)
admin.site.register(HolidaySection, HolidaySectionAdmin)
admin.site.register(Registration, RegistrationAdmin)
