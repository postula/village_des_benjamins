from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from members.models import User, Child


class ChildInline(admin.TabularInline):
    model = Child
    extra = 0


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [ChildInline]
    fieldsets = [
        [None, {"fields": ["first_name", "last_name", "email",  "password", "photo"]}],
        [_("Connection"), {"fields": ["is_active", "is_staff"]}]
    ]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_staff",
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
admin.site.register(User, UserAdmin)
