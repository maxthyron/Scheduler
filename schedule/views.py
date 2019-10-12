from django.shortcuts import render, redirect
from django.core.management import call_command
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib import messages
from .models import ScheduleSubject, Auditorium, ScheduleTime, Day, ReservedAuditorium
from django.http import JsonResponse
import datetime
from . import functions


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            print("registered here")
            messages.success(request, f'Account created for {username}. Now you can log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'schedule/register.html', {'form': form})


def refresh_models(request):
    call_command('clear_models')
    data = {'refreshed': True}
    return JsonResponse(data)


def cancel_reserved(request):
    schedule_day = Day.objects.get(id=request.GET.get('day_id'))
    schedule_time = ScheduleTime.objects.get(id=request.GET.get('time_id'))
    aud = Auditorium.objects.get(id=request.GET.get('aud_id'))
    user = User.objects.get(username=request.GET.get('user'))

    reserved_auditorium = ReservedAuditorium.objects.get(day=schedule_day,
                                                         time=schedule_time,
                                                         auditorium=aud,
                                                         user=user)
    reserved_auditorium.delete()

    data = {'canceled': True}
    return JsonResponse(data)


def occupy_auditorium(request):
    schedule_day = Day.objects.get(id=request.GET.get('day_id'))
    schedule_time = ScheduleTime.objects.get(id=request.GET.get('time_id'))
    aud = Auditorium.objects.get(id=request.GET.get('aud_id'))
    user = User.objects.get(username=request.GET.get('user'))

    reserved_auditorium = ReservedAuditorium(day=schedule_day,
                                             time=schedule_time,
                                             auditorium=aud,
                                             user=user)
    reserved_auditorium.save()

    data = {'taken': True}
    return JsonResponse(data)


# @login_required()
def subject(request, day_name, time_id, aud_id):
    aud = Auditorium.objects.get(id=aud_id)
    day = Day.objects.get(name=day_name)
    current_week = functions.get_current_week()
    reserved = ReservedAuditorium.objects.filter(day=day, time_id=time_id, auditorium=aud)
    if reserved:
        user = User.objects.get(id=reserved.first().user.id)
    else:
        user = None
    subjects = ScheduleSubject.subjects.filter(day=day.id, time_id=time_id,
                                               week_interval=current_week,
                                               auditorium_id=aud_id)
    s = subjects.first()
    groups = subjects.values_list('group', flat=True)

    return render(request, 'schedule/subject.html', {'groups':           groups,
                                                     'aud':              aud,
                                                     'day':              day,
                                                     'time_id':          time_id,
                                                     'subject':          s,
                                                     'reserved':         reserved,
                                                     'reserved_by_user': user})


def current(request):
    current_day, current_time = functions.get_current_scheduletime()
    schedule_time = ScheduleTime.objects.all()
    for i in range(len(schedule_time)):
        current_scheduletime = datetime.time.fromisoformat(current_time)
        if schedule_time[i].start_time < current_scheduletime < schedule_time[i].end_time:
            day_table = Day.objects.filter(id=current_day)
            scheduletime_table = ScheduleTime.objects.filter(start_time=schedule_time[i].start_time)
            break
        elif schedule_time[(i - 1) if i > 0 else 0].end_time < current_scheduletime < schedule_time[
            i].end_time:
            day_table = Day.objects.filter(id=current_day)
            scheduletime_table = ScheduleTime.objects.filter(start_time=schedule_time[i].start_time)
            break
        else:
            day_table = Day.objects.filter(id=current_day + 1)
            scheduletime_table = ScheduleTime.objects.filter(start_time=schedule_time[0].start_time)

    current_week = functions.get_current_week()
    schedule_table = {}

    for d in day_table:
        schedule_table[d.name] = {'free': {}, 'occupied': {}, 'reserved': {}}

        for t in scheduletime_table:
            free = Auditorium.get_free_auditoriums(d, t, current_week)
            schedule_table[d.name]['free'][t.id] = free

            occupied = Auditorium.get_occupied_auditoriums(d, t, current_week)
            schedule_table[d.name]['occupied'][t.id] = occupied

            reserved = Auditorium.get_reserved_auditoriums(d, t)
            schedule_table[d.name]['reserved'][t.id] = reserved

    return render(request, 'schedule/table.html',
                  {'schedule_table': schedule_table,
                   'schedule_time':  scheduletime_table})


def table(request):
    day_table = Day.objects.all()
    time_table = ScheduleTime.objects.all()
    schedule_table = {}
    current_week = functions.get_current_week()

    for d in day_table:
        schedule_table[d.name] = {'free': {}, 'occupied': {}, 'reserved': {}}

        for t in time_table:
            free = Auditorium.get_free_auditoriums(d, t, current_week)
            schedule_table[d.name]['free'][t.id] = free

            occupied = Auditorium.get_occupied_auditoriums(d, t, current_week)
            schedule_table[d.name]['occupied'][t.id] = occupied

            reserved = Auditorium.get_reserved_auditoriums(d, t)
            schedule_table[d.name]['reserved'][t.id] = reserved

    return render(request, 'schedule/table.html',
                  {'schedule_table': schedule_table,
                   'schedule_time':  time_table})
