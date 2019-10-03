from django.shortcuts import render, redirect
from django.core.management import call_command
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import ScheduleSubject, Auditorium, ScheduleTime, Day
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponse('A new user has been successfully registered!')
    else:
        form = UserCreationForm()
    return render(request, 'schedule/register.html', {'form': form})


def sign_in(request):
    msg = []
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('user_dashboard')
            else:
                msg.append('You account has been deactivated!')
    else:
        msg.append('Invalid Login credentials, try again!')
    return render(request, 'schedule/login.html', {'errors': msg})


def refresh_models(request):
    print("Ajax")
    call_command('clear_models')
    data = {'refreshed': True}
    return JsonResponse(data)


# @login_required()
def subject(request, day, time_id, aud):
    day_id = Day.objects.filter(name=day)
    s = ScheduleSubject.subjects.filter(day=day_id, time_id=time_id, auditorium_id=aud)
    print(s)

    return render(request, 'schedule/subject.html', {'subject': s})


def table(request):
    days = Day.objects.all()
    time_table = ScheduleTime.objects.all()

    schedule_table = {}
    occupied_table = {}
    for d in days:
        schedule_table[d.name] = {}
        occupied_table[d.name] = {}
        for t in time_table:
            auds = Auditorium.objects \
                .exclude(id__in=ScheduleSubject.subjects.filter(day=d.id, time_id=t.id)
                         .values_list('auditorium', flat=True)).order_by("floor")
            occupied = Auditorium.objects \
                .filter(id__in=ScheduleSubject.subjects.filter(day=d.id, time_id=t.id)
                        .values_list('auditorium', flat=True)).order_by("floor")

            schedule_table[d.name][t.id] = []
            occupied_table[d.name][t.id] = []
            for a in auds:
                schedule_table[d.name][t.id].append(a.id)
            for o in occupied:
                occupied_table[d.name][t.id].append(o.id)

    return render(request, 'schedule/table.html',
                  {'schedule_table': schedule_table,
                   'schedule_time':  time_table,
                   'occupied_table': occupied_table})
