from django.core.management.base import BaseCommand
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from members.models import Child
from holiday.models import Registration


class Command(BaseCommand):
    help = "Archive children who are 13 years old or older"

    def handle(self, *args, **options):
        today = timezone.now().date()

        # Calculate exact date 13 years ago using dateutil
        thirteen_years_ago = today - relativedelta(years=13)

        # Find children to archive
        children_to_archive = (
            Child.objects.with_archived()
            .filter(birth_date__lte=thirteen_years_ago)
            .exclude(status="archived")
        )

        count = children_to_archive.count()

        # Cancel all future registrations for these children
        future_registrations = Registration.objects.filter(
            child__in=children_to_archive, holiday__start_date__gt=today
        ).exclude(status="cancelled")

        cancelled_count = future_registrations.update(status="cancelled")

        # Archive the children
        children_to_archive.update(status="archived")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully archived {count} children aged 13 or older"
            )
        )
        if cancelled_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Cancelled {cancelled_count} future holiday registrations"
                )
            )
