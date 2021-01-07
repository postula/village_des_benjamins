from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Section(models.Model):
    name = models.CharField(_("name"), max_length=255)
    min_age = models.DecimalField(_("minimum age"), decimal_places=2, max_digits=4)
    max_age = models.DecimalField(_("maximum age"), decimal_places=2, max_digits=4)
    educators = models.ManyToManyField(
        verbose_name=_("educator"),
        to="members.User",
        limit_choices_to={"is_staff": True},
        related_name="section",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("section")
        verbose_name_plural = _("sections")
