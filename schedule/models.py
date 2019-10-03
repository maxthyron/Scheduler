from django.db import models
import textwrap

from api import configs


class Auditorium(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    building = models.CharField(max_length=15)
    floor = models.IntegerField()


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
    week_interval = models.IntegerField()
    day = models.IntegerField()

    subjects = models.Manager()

    def __str__(self):
        return textwrap.dedent(configs.SUBJECT_BODY.format(lesson='{} {}'.format(self.type or '',
                                                                                 self.name),
                                                           startTime=self.time.start_time,
                                                           endTime=self.time.end_time,
                                                           auditorium=self.auditorium or '',
                                                           professor=self.professor or ''))
