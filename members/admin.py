import datetime
from calendar import monthrange

from django.contrib import admin
from django.db.models import F, ExpressionWrapper, DurationField, DateField, Value, DecimalField, Subquery, OuterRef
from django.db.models.functions import Extract, Now, ExtractMonth
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from ordered_model.admin import OrderedModelAdmin

from members.models import User, Child, StaffFunction
from section.models import Section


class StaffFunctionAdmin(OrderedModelAdmin):
    model = StaffFunction
    list_display = ["name", "order", "move_up_down_links"]


class ChildInline(admin.TabularInline):
    model = Child
    extra = 0


def monthdelta(d1, d2):
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += datetime.timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta


class SectionFilter(admin.SimpleListFilter):
    title = _('section')
    parameter_name = 'section'

    def lookups(self, request, model_admin):
        return [(n, n) for n in Section.objects.values_list("name", flat=True)]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(_section=value)
        return queryset


class ChildAdmin(admin.ModelAdmin):
    model = Child
    list_display = ["parent", "first_name", "last_name", "status", "section"]
    list_filter = ["parent", "status", SectionFilter]
    search_fields = ["first_name", "last_name"]
    fieldsets = [
        [None, {"fields": ["first_name", "last_name", "birth_date", "gender", "parent", "status", "section"]}]
    ]
    readonly_fields = ["section"]


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [ChildInline]
    fieldsets = [
        [None, {"fields": ["first_name", "last_name", "email",  "password", "photo", "is_active"]}],
        [_("team"), {"fields": ["is_staff", 'role', 'groups', 'visible_on_site']}]
    ]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "role",
        "photo_list_preview",
    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)
    list_filter = ["accept_newsletter", "is_staff"]

    def photo_list_preview(self, obj):
        if obj.photo:
            return mark_safe(
                '<img src="{}" width="50" height="50" />'.format(obj.photo.url)
            )
        return ""
    photo_list_preview.short_description = "Photo"


# Re-register UserAdmin
#admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(StaffFunction, StaffFunctionAdmin)
