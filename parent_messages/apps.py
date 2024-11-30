from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ParentMessageConfig(AppConfig):
    name = 'parent_messages'
    verbose_name = _('parent_messages')
