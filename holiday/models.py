import datetime
from pprint import pprint

from django.db.models import Count
from django.utils.safestring import mark_safe
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.validators import MinValueValidator
from decimal import Decimal
from logging import getLogger
from tinymce.models import HTMLField
from ordered_model.models import OrderedModel

from section.models import Section

logger = getLogger(__name__)


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
    blacklisted_dates = ArrayField(
        models.DateField(),
        verbose_name=_("blacklisted_dates"),
        default=list,
        blank=True,
        null=True,
    )
    book_by_day = models.BooleanField(default=False, verbose_name=_("book_by_day"))
    description = HTMLField(verbose_name=_("description"), blank=True, null=True)
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
        verbose_name=_("holiday"), to="holiday.Holiday", on_delete=models.CASCADE,
        related_name="holiday_sections"
    )
    capacity = models.IntegerField(_("capacity"))
    description = HTMLField(verbose_name=("description"), blank=True, null=True)

    def _remaining_capacity(self):
        # Num days is number of non weekend days in the holiday
        num_days = 0
        current_date = self.holiday.start_date
        while current_date < self.holiday.end_date:
            if current_date.weekday() > 4:
                # weekend
                current_date += datetime.timedelta(days=1)
                continue
            current_date += datetime.timedelta(days=1)
            num_days += 1
        # Total capacity is the numof days time the capacity
        max_capacity = num_days * self.capacity
        # Taken capacity is the sum of unique date registered
        taken_capacity = 0
        registrations = self.holiday.registration_set.filter(
            section=self.section
        )
        for registration in registrations:
            taken_capacity += len(registration.dates)
        remaining_capacity = 100 - (round(Decimal(taken_capacity / max_capacity), 2) * 100)
        return f"{remaining_capacity}%"
    _remaining_capacity.short_description = _("remaining capacity")
    remaining_capacity = property(_remaining_capacity)

    def _remaining_capacity_table(self):
        dates = []
        current_date = self.holiday.start_date
        while current_date < self.holiday.end_date:
            if current_date.weekday() > 4:
                # weekend
                current_date += datetime.timedelta(days=1)
                continue
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
        dates.append(current_date)
        capacities = {}
        for date in dates:
            capacities[date] = self.capacity - Registration.objects.filter(section=self.section, dates__contains=[date]).count()
        table_raw = """
            <table class="table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Capacité Restante</th>
                    </tr>
                </thead>
                <tbody>
        """
        for date in capacities:
            capacity = capacities[date]
            table_raw += f"""
                    <tr>
                        <td>{date.strftime("%d/%m/%Y")}</td/>
                        <td style="text-align: right">{capacity}</td/>
                    </tr>
                    """
        table_raw += """
                </tbody>
            </table>
        """
        return mark_safe(table_raw)
    _remaining_capacity_table.short_description = ""
    remaining_capacity_table = property(_remaining_capacity_table)

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
    notes = models.TextField(verbose_name=_("notes"), blank=True, null=True)

    def _number_of_days(self):
        return len(self.dates)

    _number_of_days.short_description = _("number of days")
    number_of_days = property(_number_of_days)

    def _cost(self):
        section_holiday = self.holiday.holiday_sections.get(section=self.section)
        outing_cost = Decimal(0.0)
        dates = self.dates
        for outing in section_holiday.outings.all():
            booked = False
            if not outing.end_date:
                if outing.start_date in dates:
                    booked = True
            else:
                for reservation_date in dates:
                    if outing.start_date <= reservation_date <= outing.end_date:
                        booked = True
                        break
            if booked:
                outing_cost += outing.price
        return round(self.number_of_days * self.holiday.price + outing_cost, 2)

    _cost.short_description = _("price")
    cost = property(_cost)

    class Meta:
        verbose_name = _("registration")
        verbose_name_plural = _("registrations")
        unique_together = [["holiday", "child"]]


class SectionProgram(models.Model):
    section_holiday = models.ForeignKey(
        to="holiday.HolidaySection",
        verbose_name=_("section_holiday"),
        on_delete=models.CASCADE,
        related_name="activities",
    )
    description = HTMLField(verbose_name=("description"), blank=True, null=True)
    # TODO: add validation
    start_date = models.DateField(_("start date"))
    end_date = models.DateField(_("end date"))
    animateur = models.ManyToManyField(
        to="members.User",
        verbose_name=_('animateur'),
        related_name="holiday_weeks"
    )
    theme = models.CharField(
        max_length=255,
        verbose_name=_('theme'), blank=True, null=True
    )
    bricolage = models.CharField(
        max_length=255,
        verbose_name=_('bricolage'), blank=True, null=True
    )
    food = models.CharField(
        max_length=255,
        verbose_name=_('food'), blank=True, null=True
    )
    game = models.CharField(
        max_length=255,
        verbose_name=_('game'), blank=True, null=True
    )
    other = models.CharField(
        max_length=255,
        verbose_name=_('other'), blank=True, null=True
    )

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"

    class Meta:
        verbose_name = _("section_program")
        verbose_name_plural = _("section_programs")
        ordering = ["start_date"]


class Outing(models.Model):
    section_holiday = models.ForeignKey(
        to="holiday.HolidaySection",
        verbose_name=_("section_holiday"),
        on_delete=models.CASCADE,
        related_name="outings",
    )
    # date = models.DateField(_("date"))
    start_date = models.DateField(_("start date"))
    end_date = models.DateField(_("end date"), blank=True, null=True)
    name = models.CharField(_("name"), max_length=255)
    description = HTMLField(verbose_name=_("description"))
    price = models.DecimalField(
        _("price"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    departure_time = models.TimeField(_("departure_time"), blank=True, null=True)
    arrival_time = models.TimeField(_("arrival_time"), blank=True, null=True)
    transport = models.CharField(_("transport"), max_length=255, blank=True, null=True)

    def clean(self):
        start_date = self.section_holiday.holiday.start_date
        end_date = self.section_holiday.holiday.end_date
        has_errors = False
        errors = {}
        if self.end_date and self.end_date < self.start_date:
            has_errors = True
            errors[
                "date"
            ] = "Le début de la sortie doit être avant la fin de la sortie"
        if self.start_date < start_date or self.start_date > end_date:
            has_errors = True
            errors[
                "date"
            ] = "La sortie doit commencée entre le {} et le {}".format(
                start_date, end_date
            )
        if self.end_date and (self.end_date < start_date or self.end_date > end_date):
            has_errors = True
            errors[
                "date"
            ] = "La sortie doit finir entre le {} et le {}".format(
                start_date, end_date
            )
        if self.departure_time and self.arrival_time and self.departure_time > self.arrival_time:
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
        ordering = ["start_date"]


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
    <title>Réservation</title>
</head>

<body>
    <h3> Bonjour {parent_name},<br></h3>
    <p>
        Nous avons bien reçu l'inscription pour les
        vacances de "{holiday_name}" pour
        {child_name}.</p>
    <p>
        {child_name} est inscrit{child_gender_accord}
        au dates suivantes:
    <ul>{date_li}</ul>
    </p>
    <p>
        Afin de finaliser l'inscription veuillez
        procéder au versement de {cost}€ sur le compte
        BE45 3631 4231 3689 en mentionant la
        communication suivante:
        "{payment_communication}"</p>
    <p>
        Merci de votre confiance,
    </p>
    <p>
        On se réjouit de voir {child_first_name} pendant les vacances!
    </p>
    <p>
        L'Équipe du Village des Benjamins</p>
    </td>
</body>

</html>
"""


def _send_registration_notification(obj):
    child_name = f"{obj.child.first_name} {obj.child.last_name}"
    parent_name = f"{obj.child.parent.first_name} {obj.child.parent.last_name}"
    payment_communication = (
        f"{child_name.lower()} vacances {obj.holiday.name.lower()}"
    )
    child_gender_accord = "e" if obj.child.gender == "female" else ""
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
    try:
        response = sg.send(message)
    except Exception as e:
        logger.exception(e)


def send_registration_notification(sender, created, **kwargs):
    if kwargs.get("raw", False):
        return
    if not created:
        return
    obj = kwargs["instance"]
    return _send_registration_notification(obj)


def create_section_holiday(sender, created, **kwargs):
    if kwargs.get("raw", False):
        return
    if not created:
        return
    obj = kwargs["instance"]
    # 1. Split by week
    weeks = []
    prev_date = obj.start_date
    start_week = prev_date
    while prev_date < obj.end_date:
        if prev_date.weekday() == 4:
            weeks.append((start_week, prev_date))
            prev_date = prev_date + datetime.timedelta(days=3)
            start_week = prev_date
        else:
            prev_date = prev_date + datetime.timedelta(days=1)
    weeks.append((start_week, prev_date))
    for section in Section.objects.all():
        hs = HolidaySection.objects.create(
            section=section,
            holiday=obj,
            capacity=20,
        )
        hs.save()
        i = 0
        for (start_date, end_date) in weeks:
            p = SectionProgram.objects.create(
                section_holiday=hs,
                start_date=start_date,
                end_date=end_date,
                # order=i
            )
            p.animateur.set(section.educators.all())
            p.save()
            i += 1


models.signals.post_save.connect(send_registration_notification, sender=Registration)
models.signals.post_save.connect(create_section_holiday, sender=Holiday)
