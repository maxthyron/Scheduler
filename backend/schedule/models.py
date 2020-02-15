from django.db import models
from django.utils import timezone

import textwrap

from api import configs


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)


class Day(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    name_short = models.CharField(max_length=3)


class ScheduleTime(models.Model):
    id = models.IntegerField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Auditorium(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    classroom = models.IntegerField()
    building = models.CharField(max_length=15)
    floor = models.IntegerField()

    @classmethod
    def get_auditorium(cls, auditorium_id):
        try:
            auditorium = cls.objects.get(id=auditorium_id)
            return auditorium
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_occupied_auditoriums(cls, d, t, current_week):
        return cls.objects.filter(id__in=ScheduleSubject.objects
                                  .filter(day=d, schedule_time=t, week_interval__in=[0, current_week])
                                  .values_list('auditorium', flat=True)
                                  ).order_by("classroom")

    @staticmethod
    def get_reserved_auditoriums(d, t, now):
        reserved = ReservedAuditorium.get_reserved_auditoriums(d, t, now).select_related('auditorium')
        return reserved

    @classmethod
    def get_free_auditoriums(cls, d, t, now, current_week=0):
        occupied_auds = cls.get_occupied_auditoriums(d, t, current_week)
        reserved_auds = ReservedAuditorium.get_reserved_auditoriums(d, t, now).values_list('auditorium', flat=True)
        return cls.objects.exclude(id__in=occupied_auds).exclude(id__in=reserved_auds).order_by("classroom")


class ReservedAuditorium(models.Model):
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    schedule_time = models.ForeignKey(ScheduleTime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reserve_date = models.DateTimeField(default=timezone.now)

    @staticmethod
    def get_reserved_auditoriums(day, schedule_time, now):
        return ReservedAuditorium.objects.filter(day=day, schedule_time=schedule_time,
                                                 reserve_date__gt=now)

    @staticmethod
    def get_reserved_auditorium(day, schedule_time, now, auditorium):
        return ReservedAuditorium.objects.filter(day=day, schedule_time=schedule_time,
                                                 reserve_date__gt=now, auditorium=auditorium).select_related("user")

    @staticmethod
    def reserve_exists(schedule_day, schedule_time, auditorium, reserve_date, user):
        return ReservedAuditorium.objects.filter(day=schedule_day, schedule_time=schedule_time,
                                                 auditorium=auditorium, reserve_date=reserve_date,
                                                 user=user).exists()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["auditorium", "day", "schedule_time", "reserve_date", "user"],
                                    name="unique-reserved-auditoriums")
        ]


class ScheduleSubject(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=150)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.PROTECT)
    professor = models.CharField(max_length=150, null=True, blank=True)
    schedule_time = models.ForeignKey(ScheduleTime, on_delete=models.PROTECT)
    group = models.CharField(max_length=50)
    week_interval = models.IntegerField()
    day = models.ForeignKey(Day, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["type", "name", "auditorium", "day", "schedule_time", "group"],
                                    name="unique-schedule-subjects")
        ]

    def __str__(self):
        return textwrap.dedent(configs.SUBJECT_BODY.format(lesson='{} {}'.format(self.type or '', self.name),
                                                           start_time=self.schedule_time.start_time,
                                                           end_time=self.schedule_time.end_time,
                                                           day=self.day,
                                                           week=self.week_interval,
                                                           group=self.group,
                                                           auditorium=self.auditorium or '',
                                                           professor=self.professor or ''))
