from django.db import models
from django.conf import settings
import textwrap

from api import configs


class Auditorium(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    building = models.CharField(max_length=15)
    floor = models.IntegerField()

    @staticmethod
    def get_free_auditorium(d, t, current_week):
        return Auditorium.objects \
            .exclude(id__in=ScheduleSubject.subjects.filter(day=d.id, time_id=t.id,
                                                            week_interval=current_week)
                     .values_list('auditorium', flat=True)).order_by("floor")

    @staticmethod
    def get_occupied_auditorium(d, t, current_week):
        return Auditorium.objects \
            .filter(id__in=ScheduleSubject.subjects.filter(day=d.id, time_id=t.id,
                                                           week_interval=current_week)
                    .values_list('auditorium', flat=True)).order_by("floor")


class Day(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    name_short = models.CharField(max_length=3)


class ScheduleTime(models.Model):
    id = models.IntegerField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()


class ScheduleSubject(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=150)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.PROTECT)
    professor = models.CharField(max_length=150, null=True, blank=True)
    time = models.ForeignKey(ScheduleTime, on_delete=models.PROTECT)
    group = models.CharField(max_length=50)
    week_interval = models.IntegerField()
    day = models.IntegerField()

    subjects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["type", "name", "auditorium", "day", "time", "group"],
                                    name="unique-subjects")
            ]

    def __str__(self):
        return textwrap.dedent(configs.SUBJECT_BODY.format(lesson='{} {}'.format(self.type or '',
                                                                                 self.name),
                                                           startTime=self.time.start_time,
                                                           endTime=self.time.end_time,
                                                           day=self.day,
                                                           week=self.week_interval,
                                                           group=self.group,
                                                           auditorium=self.auditorium or '',
                                                           professor=self.professor or ''))
