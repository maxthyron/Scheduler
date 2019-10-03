from django.core.management.base import BaseCommand
from schedule.models import ScheduleSubject, Auditorium
from api.main import get_all_groups


class Command(BaseCommand):
    def handle(self, *args, **options):
        ScheduleSubject.subjects.all().delete()
        Auditorium.objects.all().delete()
        get_all_groups("/Users/thyron/Documents/Scheduler/api/src/")
