import datetime
from tempfile import NamedTemporaryFile

from django.contrib import admin, messages
from django.http import HttpResponse
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django.utils.translation import ugettext_lazy as _
from openpyxl import Workbook
from openpyxl.styles import Alignment
from ordered_model.admin import OrderedStackedInline, OrderedInlineModelAdminMixin, OrderedModelAdmin

from holiday.models import Holiday, HolidaySection, Registration, Outing, SectionProgram
from members.models import User


class OutingInline(admin.StackedInline):
    model = Outing
    extra = 0


class SectionProgramInline(admin.StackedInline):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "animateur":
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    model = SectionProgram
    extra = 0


class HolidaySectionAdmin(admin.ModelAdmin):
    model = HolidaySection
    extra = 0
    inlines = [SectionProgramInline, OutingInline]
    list_display = ["section", "holiday", "capacity"]
    list_filter = ["section", "holiday", "capacity"]


# Register your models here.
class HolidayAdmin(admin.ModelAdmin):
    model = Holiday
    list_display = ["name", "start_date", "end_date", "price", "registration_open"]

    actions = ["export_registration"]

    def export_registration(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(
                request,
                "L'export ne fonctionne que pour une vacances à la fois",
                messages.ERROR
            )
            return
        holiday = queryset.first()
        wb = Workbook()

        ws = wb.active
        ws.title = "Inscriptions"
        # number of days
        start_date = holiday.start_date
        end_date = holiday.end_date

        ws.cell(1, 1, value=f"{holiday} ({start_date} - {end_date})").alignment = Alignment(horizontal='center', vertical='center')
        ws.cell(2, 1, value="Enfant").alignment = Alignment(horizontal='center', vertical='center')
        ws.cell(3, 1, value="Prénom").alignment = Alignment(horizontal='center', vertical='center')
        ws.cell(3, 2, value="Nom").alignment = Alignment(horizontal='center', vertical='center')
        ws.cell(3, 3, value="Date de Naissance").alignment = Alignment(horizontal='center', vertical='center')
        ws.cell(3, 4, value="Allergies").alignment = Alignment(horizontal='center', vertical='center')
        ws.merge_cells(start_row=2, end_row=2, start_column=1, end_column=4)
        ws.cell(2, 5, value="Parent").alignment = Alignment(horizontal='center', vertical='center')
        ws.cell(3, 5, value="Prénom").alignment = Alignment(horizontal='center', vertical='center')
        ws.cell(3, 6, value="Nom").alignment = Alignment(horizontal='center', vertical='center')
        ws.cell(3, 7, value="Email").alignment = Alignment(horizontal='center', vertical='center')
        ws.merge_cells(start_row=2, end_row=2, start_column=5, end_column=7)
        ws.cell(2, 8, value="Section").alignment = Alignment(horizontal='center', vertical='center')
        ws.merge_cells(start_row=2, end_row=3, start_column=8, end_column=8)
        ws.cell(2, 9, value="# jours").alignment = Alignment(horizontal='center', vertical='center')
        ws.merge_cells(start_row=2, end_row=3, start_column=9, end_column=9)
        prev_date = holiday.start_date
        num_col = 10
        while prev_date < holiday.end_date:
            if prev_date.weekday() > 4:
                # weekend
                prev_date = prev_date + datetime.timedelta(days=1)
                continue
            ws.cell(2, num_col, value=prev_date.strftime("%A"))
            ws.cell(3, num_col, value=prev_date.strftime("%d-%m-%Y"))
            prev_date = prev_date + datetime.timedelta(days=1)
            num_col += 1
        ws.merge_cells(start_row=1, end_row=1, start_column=1, end_column=num_col)
        num_row = 4
        for registration in holiday.registration_set.all():
            num_col = 1
            # Child Info
            ws.cell(num_row, num_col, value=registration.child.first_name)
            num_col += 1
            ws.cell(num_row, num_col, value=registration.child.last_name)
            num_col += 1
            ws.cell(num_row, num_col, value=registration.child.birth_date.strftime("%d-%m-%Y"))
            num_col += 1
            ws.cell(num_row, num_col, value=registration.notes)
            num_col += 1
            ws.cell(num_row, num_col, value=registration.child.parent.first_name)
            num_col += 1
            ws.cell(num_row, num_col, value=registration.child.parent.last_name)
            num_col += 1
            ws.cell(num_row, num_col, value=registration.child.parent.email)
            num_col += 1
            ws.cell(num_row, num_col, value=registration.section.name)
            num_col += 1
            ws.cell(num_row, num_col, value=registration.number_of_days)
            num_col += 1
            prev_date = holiday.start_date
            dates = list(registration.dates)
            while prev_date < holiday.end_date:
                if prev_date.weekday() > 4:
                    # weekend
                    prev_date = prev_date + datetime.timedelta(days=1)
                    continue
                if prev_date in dates:
                    ws.cell(num_row, num_col, value=1)
                prev_date = prev_date + datetime.timedelta(days=1)
                num_col += 1
            num_row += 1
        with NamedTemporaryFile() as tmp:
            wb.save(tmp.name)
            tmp.seek(0)
            response = HttpResponse(tmp, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=inscriptions.xlsx'
            return response

    export_registration.short_description = _("export_registration_desc")


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
