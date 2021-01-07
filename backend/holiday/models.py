from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.validators import MinValueValidator
from decimal import Decimal


registration_statuses = [
    ["pending", "impayée"],
    ["paid", "payée"],
    ["cancelled", "annulée"],
]


# Create your models here.
class Holiday(models.Model):
    name = models.CharField(_("name"), max_length=255)
    price = models.DecimalField(
        _("price"),
        max_digits=10,
        decimal_places=2,
        help_text=_("price per day"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    # TODO: add validation
    start_date = models.DateField(_("start date"))
    end_date = models.DateField(_("end date"))
    description = models.TextField(_("description"), blank=True, null=True)
    registration_open = models.BooleanField(_("registration open"), default=False)
    sections = models.ManyToManyField(
        verbose_name=_("sections"),
        to="section.Section",
        through="holiday.HolidaySection",
        related_name="holidays",
    )
    registrations = models.ManyToManyField(
        verbose_name=_("registrations"),
        to="members.Child",
        through="holiday.Registration",
        related_name="holidays",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("holiday")
        verbose_name_plural = _("holidays")


class HolidaySection(models.Model):
    section = models.ForeignKey(
        verbose_name=_("section"), to="section.Section", on_delete=models.CASCADE
    )
    holiday = models.ForeignKey(
        verbose_name=_("holiday"), to="holiday.Holiday", on_delete=models.CASCADE
    )
    capacity = models.IntegerField(_("capacity"))

    def _remaining_capacity(self):
        return (
            self.capacity
            - self.holiday.registration_set.filter(section=self.section).count()
        )

    _remaining_capacity.short_description = _("remaining capacity")
    remaining_capacity = property(_remaining_capacity)

    class Meta:
        verbose_name = _("section holiday")
        verbose_name_plural = _("section holidays")


class Registration(models.Model):
    holiday = models.ForeignKey(
        verbose_name=_("holiday"), to="holiday.Holiday", on_delete=models.CASCADE
    )
    child = models.ForeignKey(
        verbose_name=_("child"),
        to="members.Child",
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    section = models.ForeignKey(
        verbose_name=_("section"),
        to="section.Section",
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    status = models.CharField(
        _("status"),
        max_length=10,
        choices=registration_statuses,
        default="pending",
    )
    dates = ArrayField(models.DateField(), verbose_name=_("dates"), default=list)

    def _number_of_days(self):
        return len(self.dates)

    _number_of_days.short_description = _("number of days")
    number_of_days = property(_number_of_days)

    def _cost(self):
        return self.number_of_days * self.holiday.price

    _cost.short_description = _("price")
    cost = property(_cost)

    class Meta:
        verbose_name = _("registration")
        verbose_name_plural = _("registrations")
        unique_together = [["holiday", "child"]]


class Outing(models.Model):
    section_holiday = models.ForeignKey(
        to="holiday.HolidaySection",
        verbose_name=_("section_holiday"),
        on_delete=models.CASCADE,
        related_name="outings",
    )
    date = models.DateField(_("date"))
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField("description")
    price = models.DecimalField(
        _("price"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    departure_time = models.TimeField(_("departure_time"))
    arrival_time = models.TimeField(_("arrival_time"))
    transport = models.CharField(_("transport"), max_length=255)

    def clean(self):
        start_date = self.section_holiday.holiday.start_date
        end_date = self.section_holiday.holiday.end_date
        has_errors = False
        errors = {}
        if self.date < start_date or self.date > end_date:
            has_errors = True
            errors[
                "date"
            ] = "La sortie doit être organisée entre le {} et le {}".format(
                start_date, end_date
            )
        if self.departure_time > self.arrival_time:
            has_errors = True
            error = "L'heure de départ doit-être avant l'heure d'arrivée"
            errors[NON_FIELD_ERRORS] = error
            errors["departure_time"] = error
            errors["arrival_time"] = error
        if has_errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = _("outing")
        verbose_name_plural = _("outings")


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
    <title>New email</title>
</head>

<body>
    <h3> Bonjour, {parent_name},<br></h3>
    <p>
        Nous avons bien reçu l'inscription pour les
        vacances de {holiday_name} pour
        {child_name}.</p>
    <p>
        {child_name} est inscrit{child_gender_accord}
        au dates suivantes:
    <ul>{date_li}</ul>
    </p>
    <p>
        Afin de finaliser l'inscription veuillez
        procédér au versement de {cost}€ sur le compte
        BEXX XXXX XXXX XXXX XXXX en mentionant la
        communication suivante:
        "{payment_communication}"</p>
    <p>
        Merci de votre confiance, on se réjouit de voir
        {child_first_name} pendant les vacances de
        {holiday_name}!<br></p>
    <p>
        Amicalement vôtre,</p>
    <p>
        Le village des benjamins</p>
    </td>
</body>

</html>
"""


def send_registration_notification(sender, created, **kwargs):
    if not created:
        return
    obj = kwargs["instance"]
    child_name = f"{obj.child.first_name} {obj.child.last_name}"
    parent_name = f"{obj.child.parent.first_name} {obj.child.parent.last_name}"
    payment_communication = (
        f"reservation {obj.holiday.name.lower()} {child_name.lower()}"
    )
    child_gender_accord = "e" if obj.child.gender == "female" else "male"
    date_li = (
        "<li>" + "</li><li>".join([d.strftime("%d-%m-%Y") for d in obj.dates]) + "</li>"
    )
    html_content = html_template.format(
        holiday_name=obj.holiday.name,
        child_name=child_name,
        payment_communication=payment_communication,
        cost=obj.cost,
        child_gender_accord=child_gender_accord,
        parent_name=parent_name,
        date_li=date_li,
        child_first_name=obj.child.first_name,
    )
    message = Mail(
        from_email=settings.SENDGRID_FROM_MAIL,
        to_emails=obj.child.parent.email,
        subject=f"Réservation pour les vacances de {obj.holiday.name} pour {child_name}",
        html_content=html_content.format(
            holiday_name=obj.holiday.name,
            child_name=child_name,
            payment_communication=payment_communication,
            cost=obj.cost,
            child_gender_accord=child_gender_accord,
            parent_name=parent_name,
            date_li=date_li,
        ),
    )
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code, response.body, response.headers)


models.signals.post_save.connect(send_registration_notification, sender=Registration)