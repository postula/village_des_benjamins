from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HolidayConfig(AppConfig):
    name = "holiday"
    verbose_name = _("holiday")
