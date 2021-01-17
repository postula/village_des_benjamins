from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SiteContentConfig(AppConfig):
    name = 'site_content'
    verbose_name = _('site_content')
