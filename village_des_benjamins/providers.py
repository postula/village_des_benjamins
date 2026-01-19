from django.conf import settings
from django.core.mail import EmailMessage
from reset_password.models import EmailProvider
from logging import getLogger
import sentry_sdk


logger = getLogger(__name__)


class SMTPEmailProvider(EmailProvider):
    """Email provider using Django's SMTP backend (Fastmail)."""

    def send_email(self, email, title, content):
        try:
            message = EmailMessage(
                subject=title,
                body=content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            message.content_subtype = "html"
            message.send()
        except Exception as e:
            logger.exception(e)
            sentry_sdk.capture_exception(e)
