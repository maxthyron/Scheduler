from api import configs
import requests
import datetime
import pytz


def get_start_date():
    date = '02-09-2019'

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
