from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from logging import getLogger
from django.db import models
from django.utils.translation import gettext_lazy as _
import sentry_sdk


logger = getLogger(__name__)


class Message(models.Model):
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email"), max_length=255)
    message = models.TextField(_("message"), blank=True, null=True)

    def __str__(self):
        return self.name + self.email

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")


class Config(models.Model):
    subject = models.CharField(_("subject"), max_length=255)
    recipients = models.ManyToManyField(to="members.User")

    def __str__(self):
        return self.subject


html_thanks_template = """
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
    <title>Formulaire de contact</title>
</head>

<body>
    <h3> Bonjour {contactName},<br></h3>
    <p>
        Nous avons bien reçu votre message, et vous répondrons dés que possible.</p>
    <p>
        Amicalement vôtre,</p>
    <p>
        Le village des benjamins</p>
    </td>
</body>

</html>
"""

html_contact_template = """
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
    <title>Formulaire de contact</title>
</head>

<body>
    <h3> Bonjour, <br></h3>
    <p>
        Un nouveau message vient d'être envoyé sur le site.</p>
    <p>
        Le message provient de {contactName}: {contactMail}
    </p>
    <hr>
    <p> {contactMessage}</p>
</body>

</html>
"""


def send_message_notification(sender, created, **kwargs):
    if kwargs.get("raw", False):
        return
    if not created:
        return
    obj = kwargs["instance"]
    contactName = obj.name
    contactMail = obj.email
    contactMessage = obj.message
    html_thanks_content = html_thanks_template.format(contactName=contactName)
    html_contact_content = html_contact_template.format(
        contactName=contactName, contactMail=contactMail, contactMessage=contactMessage
    )
    thanks_message = Mail(
        from_email=settings.SENDGRID_FROM_MAIL,
        to_emails=contactMail,
        subject="Formulaire de contact",
        html_content=html_thanks_content,
    )
    contact_message = Mail(
        from_email=settings.SENDGRID_FROM_MAIL,
        to_emails=list(
            Config.objects.first().recipients.values_list("email", flat=True)
        ),
        subject=Config.objects.first().subject,
        html_content=html_contact_content,
    )
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    try:
        sg.send(thanks_message)
        sg.send(contact_message)
    except Exception as e:
        logger.exception(e)
        sentry_sdk.capture_exception(e)


models.signals.post_save.connect(send_message_notification, sender=Message)
