from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from ordered_model.admin import OrderedModelAdmin

from members.models import User, Child, StaffFunction


class StaffFunctionAdmin(OrderedModelAdmin):
    model = StaffFunction
    list_display = ["name", "order", "move_up_down_links"]


class ChildInline(admin.TabularInline):
    model = Child
    extra = 0


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [ChildInline]
    fieldsets = [
        [None, {"fields": ["first_name", "last_name", "email",  "password", "photo", "is_active"]}],
        [_("team"), {"fields": ["is_staff", 'role', 'visible_on_site']}]
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


# Re-register UserAdmin
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(StaffFunction, StaffFunctionAdmin)
