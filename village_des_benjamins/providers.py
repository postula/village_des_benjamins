from django.conf import settings
from reset_password.models import EmailProvider
from sendgrid import Mail, SendGridAPIClient
from logging import getLogger


logger = getLogger(__name__)


class SendgridEmailProvider(EmailProvider):
    def send_email(self, email, title, content):
        message = Mail(
            from_email=settings.SENDGRID_FROM_MAIL,
            to_emails=[email],
            subject=title,
            html_content=content,
        )
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        try:
            sg.send(message)
        except Exception as e:
            logger.exception(e)
