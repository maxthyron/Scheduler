from django.db import models
import textwrap

from api import configs


class Subject(models.Model):
    type = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=50)
    auditorium = models.CharField(max_length=5, null=True, blank=True)
    professor = models.CharField(max_length=50, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    week_interval = models.IntegerField()
    day = models.IntegerField()

    @classmethod
    def create(cls, info, subject_day_index, week_interval, time_interval):
        subject = cls()
        subject.type, subject.name, subject.auditorium, subject.professor = info
        subject.start_time, subject.end_time = time_interval
        subject.week_interval = week_interval
        subject.day = subject_day_index

        return subject

    def __str__(self):
        return textwrap.dedent(configs.SUBJECT_BODY.format(lesson='{} {}'.format(self.type or '',
                                                                                 self.name),
                                                           startTime=self.start_time,
                                                           endTime=self.end_time,
                                                           auditorium=self.auditorium or '',
                                                           professor=self.professor or ''))
# class Classroom(models.Model):
#     id = models.IntegerField(primary_key=True)
#     floor = models.IntegerField()
#     building = models.TextField()
#
#
# class Lesson(models.Model):
#     name = models.TextField()
#     time = models.TimeField()
#     classroomId = models.ForeignKey(Classroom, on_delete=models.PROTECT)
