from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import namedtuple

from .models import *
from .serializers import *
from . import functions

TimeTable = namedtuple('TimeTable', ('schedule_time', 'free', 'reserved', 'scheduled'))
DayTable = namedtuple('DayTable', ('schedule_day', 'time_tables'))


@api_view(['GET'])
def table(request):
    if request.method == "GET":
        days = Day.objects.all().iterator()
        schedule_times = ScheduleTime.objects.all()
        current_week = functions.get_current_week()
        now = timezone.now()
        day_tables = []
        for d in days:
            time_tables = []
            for t in schedule_times:
                reserved = ReservedAuditorium.get_reserved_auditoriums(d, t, now)
                free = Auditorium.get_free_auditoriums(d, t, now, current_week)
                scheduled = ScheduleSubject.get_scheduled_auditoriums(d, t, current_week)

                time_table = TimeTable(schedule_time=t, free=free, scheduled=scheduled, reserved=reserved)
                time_tables.append(time_table)
            day_table = DayTable(schedule_day=d, time_tables=time_tables)
            day_tables.append(day_table)
        week_table_serializer = DayTableSerializer(day_tables, many=True)
        return Response(week_table_serializer.data)
