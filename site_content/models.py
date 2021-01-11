from django.db import models
from django.utils.translation import ugettext_lazy as _


class SiteSection(models.Model):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("site_section")
        verbose_name_plural = _("site_sections")


# Create your models here.
class Content(models.Model):
    name = models.CharField(_("name"), max_length=255)
    icon = models.CharField(_("icon"), max_length=255, help_text="https://fontawesome.com/v4.7.0/icons/", blank=True, null=True)
    description = models.TextField(_("description"))
    section = models.ForeignKey(
        verbose_name=_("site_section"),
        to="site_content.SiteSection",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("content")
        verbose_name_plural = _("content")
