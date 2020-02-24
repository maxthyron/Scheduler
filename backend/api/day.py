from scheduler_app.models import ScheduleSubject, ScheduleTime, Auditorium, Day
from bs4 import BeautifulSoup as bsoup
from api.logger import LogMachine as log
from api import configs

import re
import csv


def create_schedule_timetable_csv(source_dir):
    with open(source_dir + "time_table.csv", "r") as time_table:
        reader = csv.DictReader(time_table)
        for row in reader:
            schedule_time = ScheduleTime(id=row['id'], start_time=row['start_time'],
                                         end_time=row['end_time'])
            schedule_time.save()
    log.info('Time table added')
    with open(source_dir + "day_table.csv", "r") as day_table:
        reader = csv.DictReader(day_table)
        for row in reader:
            d = Day(id=row['id'], name=row['name'], name_short=row['name_short'])
            d.save()
    log.info('Day table added')


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


def process_auditorium(a):
    if a:
        return re.findall(r"([^а-я,\W][^а-яА-Я]\d+[а-я]?)", a)
    else:
        return []


def parse_row(cells, day_object, valid_group_code):
    if len(set(cell for cell in cells[3:5])) > 1:
        subjects = []
        start_time, end_time = map(lambda x: x + ':00', cells[1].string.split(" - "))
        time_id = ScheduleTime.objects.get(start_time=start_time).id

        for c in range(3, 5):
            try:
                _type, name, auditorium_cell, professor = (cells[c].contents[i].string for i in
                                                           range(0, 7, 2))
                auditoriums = process_auditorium(auditorium_cell)
                for auditorium in auditoriums:
                    if not auditorium or auditorium == 'Каф':
                        raise AttributeError
                    elif not Auditorium.objects.filter(id=auditorium):
                        room = re.search(r'(\d+)', auditorium).group()
                        building = re.search(r'[а-я]?$', auditorium).group()
                        floor = (int(auditorium[:2] if len(room) == 4 else int(auditorium[:1])))
                        a = Auditorium(id=auditorium,
                                       classroom=room,
                                       building=building,
                                       floor=floor)
                        a.save()

                    subject = ScheduleSubject(type=_type,
                                              name=name,
                                              auditorium=Auditorium.objects.get(id=auditorium),
                                              professor=professor,
                                              group=valid_group_code,
                                              day=day_object,
                                              week_interval=
                                              (0 if cells[3].attrs == {'colspan': '2'}
                                               else 1) + (c == 4),
                                              schedule_time_id=time_id)
                    subjects.append(subject)
            except (IndexError, AttributeError):
                pass

        return subjects
