from django.core.mail.backends.smtp import EmailBackend
import os

class ReplyToEmailBackend(EmailBackend):
    def send_messages(self, email_messages):
        reply_to = os.getenv("REPLY_TO_EMAIL")
        if reply_to:
            for msg in email_messages:
                if not msg.reply_to:
                    msg.reply_to = [reply_to]
        return super().send_messages(email_messages)
