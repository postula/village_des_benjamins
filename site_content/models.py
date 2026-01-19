from colorfield.fields import ColorField
from django.db import models
from django.utils.safestring import mark_safe
from ordered_model.models import OrderedModel
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _


LAYOUT_CHOICES = [
    ("introduction", _("introduction")),
    ("contact", _("contact")),
    ("team", _("team")),
    ("list_left", _("list_left")),
    ("list_right", _("list_right")),
    ("simple_list", _("simple_list")),
]


class SiteSection(OrderedModel):
    key = models.CharField(_("key"), max_length=255)
    name = models.CharField(_("name"), max_length=255)
    description = HTMLField(verbose_name=_("description"), blank=True, null=True)
    photo = models.ImageField(null=True, blank=True, upload_to="site_sections/")
    layout = models.CharField(
        _("layout"), max_length=50, choices=LAYOUT_CHOICES, default="list_left"
    )
    background = ColorField(format="hexa")

    def __str__(self):
        return self.name

    @property
    def photo_preview(self):
        if self.photo:
            return mark_safe(
                '<img src="{}" width="300" height="300" />'.format(self.photo.url)
            )
        return ""

    class Meta(OrderedModel.Meta):
        verbose_name = _("site_section")
        verbose_name_plural = _("site_sections")


# Create your models here.
class Content(OrderedModel):
    name = models.CharField(_("name"), max_length=255)
    icon = models.CharField(
        _("icon"),
        max_length=255,
        help_text="https://fontawesome.com/v4.7.0/icons/",
        blank=True,
        null=True,
    )
    description = HTMLField(verbose_name=("description"))
    show_more_button = models.CharField(
        _("show_more_button"), max_length=255, null=True, blank=True
    )
    show_more_content = HTMLField(
        verbose_name=_("show_more_content"), null=True, blank=True
    )
    section = models.ForeignKey(
        verbose_name=_("site_section"),
        to="site_content.SiteSection",
        on_delete=models.CASCADE,
    )
    order_with_respect_to = "section"

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        verbose_name = _("content")
        verbose_name_plural = _("content")


class ContentPlanning(models.Model):
    """
    Activity planning entries for content sections.
    Replaces HTML table storage with structured data.
    """

    SECTION_CHOICES = [
        ("maternelle", _("Les maternelles")),
        ("primaire", _("Les primaires")),
    ]

    content = models.ForeignKey(
        verbose_name=_("content"),
        to="site_content.Content",
        on_delete=models.CASCADE,
        related_name="planning_entries",
    )

    section = models.CharField(
        verbose_name=_("section"),
        max_length=20,
        choices=SECTION_CHOICES,
        null=True,
        blank=True,
    )

    educator = models.ForeignKey(
        verbose_name=_("educator"),
        to="members.User",
        on_delete=models.PROTECT,
        limit_choices_to={"is_staff": True, "visible_on_site": True},
        null=True,
        blank=True,
    )

    date = models.DateField(
        verbose_name=_("date"),
        db_index=True,
    )

    description = models.TextField(
        verbose_name=_("description"),
        max_length=500,
        blank=True,
        null=True,
        help_text=_("Activity description (max 500 characters)"),
    )

    def __str__(self):
        return f"{self.date} - {self.get_section_display()} - {self.educator}"

    class Meta:
        verbose_name = _("content planning")
        verbose_name_plural = _("content planning")
        ordering = ["date", "section"]

        constraints = [
            models.UniqueConstraint(
                fields=["content", "date", "section", "educator"],
                name="unique_planning_entry",
            )
        ]

        indexes = [
            models.Index(fields=["content", "date"]),
            models.Index(fields=["date", "section"]),
        ]


class News(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description = HTMLField(verbose_name=_("description"))

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = _("news")
        verbose_name_plural = _("news")
