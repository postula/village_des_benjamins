from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SectionConfig(AppConfig):
    name = 'section'
    verbose_name = _('section')
