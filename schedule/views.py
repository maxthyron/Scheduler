from django.shortcuts import render, redirect
from django.core.management import call_command
from .forms import UserRegisterForm
from django.contrib import messages
from .models import ScheduleSubject, Auditorium, ScheduleTime, Day
from django.http import JsonResponse
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


def occupy_auditorium(request):
    day_id = request.GET.get('day_id')
    time_id = request.GET.get('time_id')
    aud_id = request.GET.get('aud_id')
    user = request.GET.get('user')

    s = ScheduleSubject(type='(user)',
                        name=user,
                        auditorium=Auditorium.objects.get(id=aud_id),
                        professor='',
                        group=user,
                        day=day_id,
                        week_interval=-1,
                        time_id=time_id)
    s.save()

    data = {'taken': True}
    return JsonResponse(data)


# @login_required()
def subject(request, day_name, time_id, aud_id):
    aud = Auditorium.objects.get(id=aud_id)
    day = Day.objects.get(name=day_name)
    current_week = functions.get_current_week()
    subjects = ScheduleSubject.subjects.filter(day=day.id, time_id=time_id,
                                               week_interval=current_week,
                                               auditorium_id=aud_id)
    s = subjects.first()
    groups = subjects.values_list('group', flat=True)

    return render(request, 'schedule/subject.html', {'groups':  groups,
                                                     'aud':     aud,
                                                     'day':     day,
                                                     'time_id': time_id,
                                                     'subject': s})

def table(request):
    day_table = Day.objects.all()
    time_table = ScheduleTime.objects.all()
    schedule_table = {}
    current_week = functions.get_current_week()

    for d in day_table:
        schedule_table[d.name] = {'free': {}, 'occupied': {}}

        for t in time_table:
            free = Auditorium.get_free_auditorium(d, t, current_week)
            schedule_table[d.name]['free'][t.id] = free

            occupied = Auditorium.get_occupied_auditorium(d, t, current_week)
            schedule_table[d.name]['occupied'][t.id] = occupied

    return render(request, 'schedule/table.html',
                  {'schedule_table': schedule_table,
                   'schedule_time':  time_table})
