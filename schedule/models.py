from django.db import models
import textwrap

from api import configs


class ScheduleTime(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()


class ScheduleSubject(models.Model):
    type = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=50)
    auditorium = models.CharField(max_length=5)
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
        subject.time_id = time_id
        subject.week_interval = week_interval
        subject.day = subject_day_index

        return subject

    def __str__(self):
        schedule_time = ScheduleTime.objects.get(id=self.time_id)
        return textwrap.dedent(configs.SUBJECT_BODY.format(lesson='{} {}'.format(self.type or '',
                                                                                 self.name),
                                                           startTime=schedule_time.start_time,
                                                           endTime=schedule_time.end_time,
                                                           auditorium=self.auditorium or '',
                                                           professor=self.professor or ''))
