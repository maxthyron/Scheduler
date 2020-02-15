from django.http import JsonResponse
from django.db import IntegrityError
from django.utils import timezone

import bcrypt
import json

from .models import ScheduleSubject, Auditorium, ScheduleTime, Day, ReservedAuditorium, User
from . import functions


def register(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)["obj"]
        except KeyError:
            return JsonResponse({"error": "Provided JSON file is incorrect."})

        try:
            hashed_password = bcrypt.hashpw((body["password"]).encode(), bcrypt.gensalt())
        except KeyError:
            return JsonResponse({"error": "Password is not provided."})
        try:
            user = User(username=body['username'], password=hashed_password.decode())
            user.save()
            return JsonResponse({"error": None})
        except IntegrityError:
            return JsonResponse({"error": "User with such username already exists."})


def login(request, username):
    if request.method == "POST":
        try:
            body = json.loads(request.body)["obj"]
        except KeyError:
            return JsonResponse({"error": "Provided JSON file is incorrect."})

        try:
            user = User.objects.get(username=username)
            if bcrypt.checkpw(body['password'].encode(), user.password.encode()):
                return JsonResponse({"error": None})
            else:
                return JsonResponse({"error": "Password is not matching this username."})
        except User.DoesNotExist:
            return JsonResponse({"error": "User with such username doesn't exist."})
        except KeyError:
            return JsonResponse({"error": "Password is not provided."})


def reserve_auditorium(request, auditorium_id):
    if request.method == "POST":
        day, schedule_time, user = functions.parse_reserve_body(request)
        reserve_date = functions.get_reserve_date(day=day, schedule_time=schedule_time)
        auditorium = Auditorium.get_auditorium(auditorium_id=auditorium_id)
        if not auditorium:
            return JsonResponse({"error": f"{auditorium_id} auditorium does not exist."})

        if ReservedAuditorium.reserve_exists(day, schedule_time, auditorium, reserve_date, user):
            return JsonResponse({"error": "This auditorium is already reserved."})
        else:
            reserved_auditorium = ReservedAuditorium(day=day, schedule_time=schedule_time,
                                                     auditorium=auditorium, reserve_date=reserve_date,
                                                     user=user)
            reserved_auditorium.save()
            return JsonResponse({"error": None})


def unreserve_auditorium(request, auditorium_id):
    if request.method == "POST":
        day, schedule_time, user = functions.parse_reserve_body(request)
        reserve_date = functions.get_reserve_date(day=day, schedule_time=schedule_time)
        auditorium = Auditorium.get_auditorium(auditorium_id=auditorium_id)
        if not auditorium:
            return JsonResponse({"error": f"{auditorium_id} auditorium does not exist."})

        if not ReservedAuditorium.reserve_exists(day, schedule_time, auditorium, reserve_date, user):
            return JsonResponse({"error": f"This auditorium is not reserved by {user.username}."})
        else:
            reserved_auditorium = ReservedAuditorium.objects.filter(day=day, schedule_time=schedule_time,
                                                                    auditorium=auditorium, reserve_date=reserve_date,
                                                                    user=user).latest("reserve_date")
            reserved_auditorium.delete()
            return JsonResponse({"error": None})


def auditorium_info(request, auditorium_id):
    if request.method == "GET":
        auditorium = Auditorium.get_auditorium(auditorium_id=auditorium_id)
        if not auditorium:
            return JsonResponse({"error": f"{auditorium_id} auditorium does not exist."})

        day_name = request.GET.get("aud_day", "")
        if day_name:
            try:
                day = Day.objects.get(name=day_name)
            except Day.DoesNotExist:
                return JsonResponse({"data": {"error": "Name of the day is incorrect."}})
        else:
            return JsonResponse({"data": {"error": "Name of the day is not provided."}})

        time_id = request.GET.get("aud_time", "")
        if time_id:
            try:
                schedule_time = ScheduleTime.objects.get(id=time_id)
            except ScheduleTime.DoesNotExist:
                return JsonResponse({"data": {"error": "Time id is incorrect."}})
        else:
            return JsonResponse({"data": {"error": "Time is not provided."}})

        now = timezone.now()
        current_week = functions.get_current_week()

        reserved = ReservedAuditorium.get_reserved_auditorium(day=day, schedule_time=schedule_time,
                                                              now=now, auditorium=auditorium)
        form = "not_occupied"
        subject_type = None
        subject_name = None
        groups = []
        if reserved:
            form = "occupied_by_user"
            username = reserved.first().user.username
        else:
            username = None
            subjects = ScheduleSubject.objects.filter(day=day, week_interval__in=[0, current_week],
                                                      schedule_time=schedule_time, auditorium=auditorium)
            if subjects:
                form = "occupied"
                subject = subjects.first()
                subject_type = subject.type
                subject_name = subject.name
                groups = list(subjects.values_list('group', flat=True))

        return JsonResponse({'data': {'form': form,
                                      'username': username,
                                      'subject': {"type": subject_type, "name": subject_name},
                                      'groups': groups,
                                      'error': None}
                             })


def table(request):
    if request.method == "GET":
        days = Day.objects.all().iterator(chunk_size=5000)
        schedule_times = ScheduleTime.objects.all().iterator(chunk_size=5000)
        current_week = functions.get_current_week()
        now = timezone.now()
        data = []

        for d in days:
            data.append({"day": d.name, "array": []})
            free_auditoriums = {
                "state": "free",
                "array": []
            }
            occupied_auditoriums = {
                "state": "occupied",
                "array": []
            }
            reserved_auditoriums = {
                "state": "reserved",
                "array": []
            }

            for t in schedule_times:
                reserved = Auditorium.get_reserved_auditoriums(d, t, now)
                classes = [auditoriums for auditoriums in reserved.values("auditorium_id", "user_id")]
                for c in classes:
                    c["id"] = c.pop("auditorium_id")
                reserved_object = {"time": t.id, "classes": classes}

                free = Auditorium.get_free_auditoriums(d, t, now, current_week)
                free_object = {"time": t.id, "classes": [auditoriums for auditoriums in free.values("id")]}
                occupied = Auditorium.get_occupied_auditoriums(d, t, current_week)
                occupied_object = {"time": t.id, "classes": [auditoriums for auditoriums in occupied.values("id")]}

                free_auditoriums["array"].append(free_object)
                occupied_auditoriums["array"].append(occupied_object)
                reserved_auditoriums["array"].append(reserved_object)

            data[-1]["array"].append(free_auditoriums)
            data[-1]["array"].append(occupied_auditoriums)
            data[-1]["array"].append(reserved_auditoriums)

        return JsonResponse({"data": data})
