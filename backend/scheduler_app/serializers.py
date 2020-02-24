from rest_framework import serializers

from .models import Day, ScheduleTime, Auditorium, ReservedAuditorium, ScheduleSubject


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['id', 'name', 'name_short']


class SchedulerTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleTime
        fields = ['id', 'start_time', 'end_time']


class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = ['id', 'classroom', 'building', 'floor']


class ReservedAuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedAuditorium
        fields = ['auditorium', 'day', 'schedule_time', 'user', 'reserve_date']


class ScheduleSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleSubject
        fields = ['type', 'name', 'auditorium', 'professor', 'schedule_time', 'group', 'week_interval', 'day']


class TimeTableSerializer(serializers.Serializer):
    schedule_time = SchedulerTimeSerializer()
    free = AuditoriumSerializer(many=True)
    reserved = ReservedAuditoriumSerializer(many=True)
    scheduled = AuditoriumSerializer(many=True)


class DayTableSerializer(serializers.Serializer):
    schedule_day = DaySerializer()
    time_tables = TimeTableSerializer(many=True)

