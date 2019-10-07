from django.contrib import admin

from .models import ScheduleSubject, Auditorium, ScheduleTime, Day

admin.site.register(ScheduleSubject)
admin.site.register(Auditorium)
admin.site.register(ScheduleTime)
admin.site.register(Day)
