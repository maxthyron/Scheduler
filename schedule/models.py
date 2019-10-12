from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
import textwrap

from api import configs


class Auditorium(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    classroom = models.IntegerField()
    building = models.CharField(max_length=15)
    floor = models.IntegerField()

    @staticmethod
    def get_occupied_auditoriums(d, t, current_week):
        return Auditorium.objects \
            .filter(id__in=ScheduleSubject.subjects.filter(day=d.id, time_id=t.id,
                                                           week_interval__in=[0, current_week])
                    .values_list('auditorium', flat=True)).order_by("classroom")

    @staticmethod
    def get_reserved_auditoriums(d, t):
        reserved = ReservedAuditorium.objects.select_related('auditorium').filter(day_id=d.id,
                                                                                  time_id=t.id)
        return reserved

    @classmethod
    def get_free_auditoriums(cls, d, t, current_week):
        occupied_auds = cls.get_occupied_auditoriums(d, t, current_week)
        reserved_auds = ReservedAuditorium.get_reserved_auditorium(d, t)
        return Auditorium.objects \
            .exclude(id__in=occupied_auds).exclude(id__in=reserved_auds).order_by("classroom")


class Day(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    name_short = models.CharField(max_length=3)


class ScheduleTime(models.Model):
    id = models.IntegerField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()


class ReservedAuditorium(models.Model):
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    time = models.ForeignKey(ScheduleTime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    @staticmethod
    def get_reserved_auditorium(d, t):
        return ReservedAuditorium.objects.filter(day_id=d.id, time_id=t.id) \
            .values_list('auditorium', flat=True)


class ScheduleSubject(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=150)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.PROTECT)
    professor = models.CharField(max_length=150, null=True, blank=True)
    time = models.ForeignKey(ScheduleTime, on_delete=models.PROTECT)
    group = models.CharField(max_length=50)
    week_interval = models.IntegerField()
    day = models.ForeignKey(Day, on_delete=models.PROTECT)

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
