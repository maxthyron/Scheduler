from django.shortcuts import render
from .models import ScheduleSubject


def index(request):
    subjects = ScheduleSubject.objects.all()
    return render(request, 'schedule/index.html', {'subjects': subjects})


def table(request):
    return render(request, 'schedule/table.html', {})
