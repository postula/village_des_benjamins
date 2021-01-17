from django.db import models
from ordered_model.models import OrderedModel
from tinymce.models import HTMLField
from django.utils.translation import ugettext_lazy as _


class SiteSection(models.Model):
    key = models.CharField(_("key"), max_length=255)
    name = models.CharField(_("name"), max_length=255)
    description = HTMLField(verbose_name=("description"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("site_section")
        verbose_name_plural = _("site_sections")


# Create your models here.
class Content(OrderedModel):
    name = models.CharField(_("name"), max_length=255)
    icon = models.CharField(_("icon"), max_length=255, help_text="https://fontawesome.com/v4.7.0/icons/", blank=True, null=True)
    description = HTMLField(verbose_name=("description"))
    show_more_button = models.CharField(_("show_more_button"), max_length=255, null=True, blank=True)
    show_more_content = HTMLField(verbose_name=_("show_more_content"), null=True, blank=True)
    section = models.ForeignKey(
        verbose_name=_("site_section"),
        to="site_content.SiteSection",
        on_delete=models.CASCADE
    )
    order_with_respect_to = "section"

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        verbose_name = _("content")
        verbose_name_plural = _("content")


class News(models.Model):
    date = models.DateField(auto_now_add=True)
    description = HTMLField(verbose_name=_("description"))

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = _("news")
        verbose_name_plural = _("news")
