from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import namedtuple

from .models import *
from .serializers import *
from . import functions

TimeTable = namedtuple('TimeTable', ('schedule_time', 'free', 'reserved', 'scheduled'))
AuditoriumsTable = namedtuple('AuditoriumsTable', ('free', 'reserved'))
DayTable = namedtuple('DayTable', ('schedule_day', 'time_tables'))


class DayViewSet(viewsets.ViewSet):
    def list(self, request):
        days = Day.objects.all()
        days_serializer = DaySerializer(days, many=True)
        return Response(days_serializer.data)


class TimeViewSet(viewsets.ViewSet):
    def list(self, request):
        schedule_times = ScheduleTime.objects.all()
        schedule_times_serializer = SchedulerTimeSerializer(schedule_times, many=True)
        return Response(schedule_times_serializer.data)


@api_view(['GET'])
def table(request):
    if request.method == "GET":
        schedule_time_id = request.query_params.get('timeId')
        schedule_day_id = request.query_params.get('dayId')
        d = Day.objects.get(id=schedule_day_id)
        t = ScheduleTime.objects.get(id=schedule_time_id)
        current_week = functions.get_current_week()
        now = timezone.now()

        free = Auditorium.get_free_auditoriums(d, t, now, current_week)
        auditoriums_serializer = AuditoriumSerializer(free, many=True)

        return Response(auditoriums_serializer.data)


