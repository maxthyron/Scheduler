from django.utils import timezone
from django.http import JsonResponse

import datetime
import pytz
import json

from scheduler_api import configs
from .models import ScheduleTime, Day, User


def get_reserve_date(day, schedule_time):
    reserve_date = timezone.now()
    reserve_date += datetime.timedelta((day.id - reserve_date.weekday()) % 7)
    reserve_time = schedule_time.end_time
    reserve_date = reserve_date.replace(hour=reserve_time.hour, minute=reserve_time.minute,
                                        second=reserve_time.second, microsecond=0)

    return reserve_date


def get_start_date():
    date = '03-02-2020'

    return datetime.datetime.strptime(date, configs.DATE_FORMAT).date()


def get_current_week():
    date = datetime.datetime.now().astimezone(pytz.timezone('Europe/Moscow')).date()
    start_date = get_start_date()
    current_week = ((date - start_date).days // 7) % 2 + 1
    return current_week


def get_current_scheduletime():
    current_day = datetime.date.today().weekday()
    current_time = datetime.datetime.now().astimezone(pytz.timezone('Europe/Moscow')) \
        .strftime(configs.TIME_FORMAT)

    return current_day, current_time


def parse_reserve_body(request):
    try:
        body = json.loads(request.body)['obj']
        schedule_day = Day.objects.get(name=body['day'])
        schedule_time = ScheduleTime.objects.get(id=int(body['time']))
        user = User.objects.get(username=body['username'])
    except KeyError:
        return JsonResponse({"error": "Provided JSON file is incorrect."})
    except Day.DoesNotExist:
        return JsonResponse({"error": "Day id is incorrect."})
    except ScheduleTime.DoesNotExist:
        return JsonResponse({"error": "Time id is incorrect."})
    except User.DoesNotExist:
        return JsonResponse({"error": "Such user doesn't exist."})

    return schedule_day, schedule_time, user
