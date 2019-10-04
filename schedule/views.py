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
def subject(request, day_name, time_id, aud_id):
    aud = Auditorium.objects.get(id=aud_id)
    day = Day.objects.get(name=day_name)
    s = ScheduleSubject.subjects.filter(day=day.id, time_id=time_id, auditorium_id=aud_id)
    print(s)

    return render(request, 'schedule/subject.html', {'subjects': s, 'aud': aud})


def table(request):
    day_table = Day.objects.all()
    time_table = ScheduleTime.objects.all()
    schedule_table = {}
    for d in day_table:
        schedule_table[d.name] = {'free': {}, 'occupied': {}}

        for t in time_table:
            free = Auditorium.get_free_auditorium(d, t)
            schedule_table[d.name]['free'][t.id] = free

            occupied = Auditorium.get_occupied_auditorium(d, t)
            schedule_table[d.name]['occupied'][t.id] = occupied

    return render(request, 'schedule/table.html',
                  {'schedule_table': schedule_table,
                   'schedule_time':  time_table})
