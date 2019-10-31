from django.core.management.base import BaseCommand
from schedule.models import ScheduleSubject
from run import get_all_groups


class Command(BaseCommand):
    def handle(self, *args, **options):
        ScheduleSubject.subjects.all().delete()
        get_all_groups(silent=True)
