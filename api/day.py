import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbproject.settings")
import django

django.setup()

from schedule.models import ScheduleSubject, ScheduleTime, Auditorium, Day
from bs4 import BeautifulSoup as bsoup
from api.logger import LogMachine as log
from api import configs


def create_schedule_timetable(outdir):
    with open(outdir + "schedule.html", "r") as page_html:
        soup = bsoup(page_html, "lxml")
        days = soup.select('div.col-md-6.hidden-xs')
        for i, row in enumerate((days[0].contents[1]).findAll('tr')[2:]):
            day_table = (row.contents[1]).contents[0]
            start_time, end_time = map(lambda x: x + ':00', day_table.split(" - "))
            schedule_time = ScheduleTime(id=i, start_time=start_time, end_time=end_time)
            schedule_time.save()
            log.info("%d %s" % (i, day_table))

        for i, day in enumerate(days):
            name_short = day.contents[1].findAll('tr')[0].contents[1].contents[0].string
            name = configs.DAY_MAP[name_short]
            d = Day(id=i, name=name, name_short=name_short)
            d.save()


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
                elif not Auditorium.objects.filter(id=auditorium):
                    building = (auditorium[-1:] if not ("0" <= auditorium[-1:] <= "9") else "")
                    length = (len(auditorium) if not building else len(auditorium[:-1]))
                    floor = (int(auditorium[:2] if length == 4 else int(auditorium[:1])))
                    a = Auditorium(id=auditorium, building=building, floor=floor)
                    a.save()

                subject = ScheduleSubject.create(_type=_type,
                                                 name=name,
                                                 auditorium=Auditorium.objects.get(id=auditorium),
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
