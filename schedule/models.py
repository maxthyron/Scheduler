from django.db import models
import textwrap

from api import configs


class Auditorium(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    building = models.CharField(max_length=10)
    floor = models.IntegerField()


class ScheduleTime(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()


class ScheduleSubject(models.Model):
    type = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=50)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.PROTECT)
    professor = models.CharField(max_length=50, null=True, blank=True)
    time = models.ForeignKey(ScheduleTime, on_delete=models.PROTECT)
    week_interval = models.IntegerField()
    day = models.IntegerField()

    @classmethod
    def create(cls, _type, name, auditorium, professor, subject_day_index, week_interval,
               time_id):
        subject = cls()
        subject.type = _type
        subject.name = name
        subject.auditorium = auditorium
        subject.professor = professor
        subject.time = ScheduleTime.objects.get(id=time_id)
        subject.week_interval = week_interval
        subject.day = subject_day_index

        return subject

    def __str__(self):
        return textwrap.dedent(configs.SUBJECT_BODY.format(lesson='{} {}'.format(self.type or '',
                                                                                 self.name),
                                                           startTime=self.time.start_time,
                                                           endTime=self.time.end_time,
                                                           auditorium=self.auditorium or '',
                                                           professor=self.professor or ''))
