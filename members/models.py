from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from calendar import monthrange
from datetime import date, datetime, timedelta
from section.models import Section
from ordered_model.models import OrderedModel


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    photo = models.ImageField(null=True, blank=True, upload_to="members/")
    role = models.ForeignKey(verbose_name=_("role"), to="members.StaffFunction", null=True, blank=True, on_delete=models.SET_NULL)
    visible_on_site = models.BooleanField(verbose_name=_("visible_on_site"), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else self.email
        )

    @property
    def photo_list_preview(self):
        if self.photo:
            return mark_safe(
                '<img src="{}" width="50" height="50" />'.format(self.photo.url)
            )
        return ""

    @property
    def photo_preview(self):
        if self.photo:
            return mark_safe(
                '<img src="{}" width="300" height="300" />'.format(self.photo.url)
            )
        return ""

    class Meta:
        verbose_name = _("member")
        verbose_name_plural = _("members")


def monthdelta(d1, d2):
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta


class Child(models.Model):
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    birth_date = models.DateField(_("birth date"))
    gender = models.CharField(
        _("gender"),
        choices=[("male", _("male")), ("female", _("female"))],
        max_length=6,
    )
    parent = models.ForeignKey(
        verbose_name=_("parent"),
        related_name="children",
        to="members.User",
        on_delete=models.CASCADE,
    )

    @property
    def age(self):
        today = date.today()
        return monthdelta(self.birth_date, today) / 12.0

    @property
    def section(self):
        age = self.age
        section = Section.objects.filter(min_age__lte=age, max_age__gt=age)
        if section.exists():
            return section.first()
        return None

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.section if self.section else 'Aucun groupe disponible'})"

    class Meta:
        verbose_name = _("child")
        verbose_name_plural = _("children")


class StaffFunction(OrderedModel):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        verbose_name = _("staff_function")
        verbose_name_plural = _("staff_functions")
