from logging import getLogger

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    ExpressionWrapper,
    Value,
    DateField,
    F,
    DurationField,
    DecimalField,
    OuterRef,
    Subquery,
)
from django.db.models.functions import Extract
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from calendar import monthrange
from datetime import date, datetime, timedelta

from sendgrid import SendGridAPIClient, Mail

from section.models import Section
from ordered_model.models import OrderedModel

from django.conf import settings


logger = getLogger(__name__)


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

    def delete(self):
        from django_rest_passwordreset.models import ResetPasswordToken

        # Get all user IDs before deletion
        user_ids = list(self.values_list("id", flat=True))
        # Delete related tokens
        ResetPasswordToken.objects.filter(user_id__in=user_ids).delete()
        super().delete()


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    photo = models.ImageField(null=True, blank=True, upload_to="members/")
    role = models.ForeignKey(
        verbose_name=_("role"),
        to="members.StaffFunction",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    visible_on_site = models.BooleanField(
        verbose_name=_("visible_on_site"), default=False
    )
    accept_newsletter = models.BooleanField(
        verbose_name=_("accept_newsletter"), default=False
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        if self.first_name:
            if self.last_name:
                return f"{self.first_name} {self.last_name}"
            return self.first_name
        return self.email

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


class ChildManager(models.Manager):
    def get_date_queryset(self, check_date):
        qs = super().get_queryset()
        age_expr = ExpressionWrapper(
            Value(check_date, DateField()) - F("birth_date"),
            output_field=DurationField(),
        )
        qs = qs.annotate(
            _age_inter=age_expr,
            _age_epoch=Extract("_age_inter", "epoch"),
            _age=ExpressionWrapper(
                F("_age_epoch") / Value(31556952, output_field=DecimalField()),
                output_field=DecimalField(decimal_places=1),
            ),
            _section=Subquery(
                Section.objects.filter(
                    min_age__lte=OuterRef("_age"), max_age__gt=OuterRef("_age")
                ).values("name")
            ),
        )
        return qs

    def get_queryset(self):
        return self.get_date_queryset(datetime.today())


class Child(models.Model):
    objects = ChildManager()
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
    status = models.CharField(
        _("status"),
        choices=[
            ("in_validation", _("in_validation")),
            ("registered", _("registered")),
        ],
        max_length=50,
        default="in_validation",
    )

    @property
    def age(self):
        today = date.today()
        return monthdelta(self.birth_date, today) / 12.0

    @property
    def section(self):
        # if already set (e.g. by view), skip DB
        if hasattr(self, "_section"):
            return self._section

        # one‐time load per process/request
        cls = self.__class__
        if not hasattr(cls, "_sections_cache"):
            cls._sections_cache = list(Section.objects.all())

        age = self.age
        for sec in cls._sections_cache:
            if sec.min_age <= age < sec.max_age:
                self._section = sec
                return sec

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


html_template = """
<!DOCTYPE html
    PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office"
    style="width:100%;font-family:arial, 'helvetica neue', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">

<head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title>Inscription</title>
</head>

<body>
    <h3> Bonjour {name},<br></h3>
    <p>
    Bienvenue sur le site internet du Village des Benjamins.
    </p>
    <p>
    Merci de votre inscription, vous pouvez maintenant vous connecter et ajouter votre/vos enfant(s).
    </p>
    <p>
        L'Équipe du Village des Benjamins</p>
    </td>
</body>

</html>
"""


def send_registration_notification(sender, created, **kwargs):
    if kwargs.get("raw", False):
        return
    if not created:
        return
    obj = kwargs["instance"]
    name = str(obj)
    html_content = html_template.format(
        name=name,
    )
    message = Mail(
        from_email=settings.SENDGRID_FROM_MAIL,
        to_emails=obj.email,
        subject=f"Inscription sur le site du Village des Benjamins",
        html_content=html_content,
    )
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    try:
        response = sg.send(message)
    except Exception as e:
        logger.exception(e)


models.signals.post_save.connect(send_registration_notification, sender=User)
