from django.shortcuts import render
from .models import Subject


def index(request):
    subjects = Subject.objects.all()
    return render(request, 'schedule/index.html', {'subjects': subjects})


def table(request):
    return render(request, 'schedule/table.html', {})
