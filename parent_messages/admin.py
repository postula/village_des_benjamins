from django.contrib import admin
from parent_messages.models import Message, Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    model = Config
    list_display = ["subject"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ["name", "email", "message"]


# Register your models here.
