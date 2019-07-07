import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbproject.settings")
import django

django.setup()

from schedule.models import ScheduleSubject, ScheduleTime
from bs4 import BeautifulSoup as bsoup
from api.logger import LogMachine as log


def create_schedule_time(outdir):
    with open(outdir + "schedule.html", "r") as page_html:
        soup = bsoup(page_html, "lxml")
        day = soup.select('div.col-md-6.hidden-xs')[0]
        for i, row in enumerate((day.contents[1]).findAll('tr')[2:]):
            day_table = (row.contents[1]).contents[0]
            start_time, end_time = map(lambda x: x + ':00', day_table.split(" - "))
            schedule_time = ScheduleTime(id=i, start_time=start_time, end_time=end_time)
            schedule_time.save()
            log.info("%d %s" % (i, day_table))


def parse_row(cells, day_number):
    if len(set(cell for cell in cells[3:5])) > 1:
        subjects = []
        start_time, end_time = map(lambda x: x + ':00', cells[1].string.split(" - "))
        time_id = ScheduleTime.objects.get(start_time=start_time).id

        for c in range(3, 5):
            try:
                _type, name, auditorium, professor = (cells[c].contents[i].string for i in range(
                    0, 7, 2))
                if not auditorium or auditorium == 'Каф':
                    raise AttributeError

                subject = ScheduleSubject.create(_type=_type,
                                                 name=name,
                                                 auditorium=auditorium,
                                                 professor=professor,
                                                 subject_day_index=day_number,
                                                 week_interval=
                                                 (0 if cells[3].attrs == {
                                                     'colspan': '2'} else 1) + (c == 4)
                                                 ,
                                                 time_id=time_id)
                subjects.append(subject)
            except (IndexError, AttributeError):
                pass

        return subjects
