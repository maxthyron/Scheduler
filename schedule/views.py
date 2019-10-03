from django.shortcuts import render
from django.core.management import call_command
from .models import ScheduleSubject, Auditorium, ScheduleTime, Day
from django.http import JsonResponse, HttpResponse


def index(request):
    subjects = ScheduleSubject.subjects.all().select_related()

    return render(request, 'schedule/index.html', {'subjects': subjects})

def refresh_models(request):
    print("Ajax")
    call_command('clear_models')
    data = {'refreshed': True}
    return JsonResponse(data)

def table(request):
    days = Day.objects.all()
    time_table = ScheduleTime.objects.all()

    schedule_table = {}
    for d in days:
        schedule_table[d.name] = {}
        for t in time_table:
            auds = Auditorium.objects \
                .exclude(id__in=ScheduleSubject.subjects.filter(day=d.id,
                                                                time_id=t.id)
                         .values_list('auditorium', flat=True)).order_by("id")

            schedule_table[d.name][t.id] = []
            for a in auds:
                schedule_table[d.name][t.id].append(a.id)

    return render(request, 'schedule/table.html',
                  {'schedule_table': schedule_table,
                   'schedule_time':  time_table})
