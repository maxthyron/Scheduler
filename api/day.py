import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbproject.settings")
import django

django.setup()

from schedule.models import Subject


def parse_row(cells, day_number):
    if len(set(cell for cell in cells[3:5])) > 1:
        subjects = []
        timing = cells[1].string

        for c in range(3, 5):
            try:
                subject = Subject.create(info=(cells[c].contents[i].string for i in range(0, 7, 2)),
                                         subject_day_index=day_number,
                                         week_interval=
                                         (0 if cells[3].attrs == {'colspan': '2'} else 1) + (c == 4)
                                         ,
                                         time_interval=map(lambda x: x + ":00",
                                                           timing.split(' - ')))
                subjects.append(subject)
            except (IndexError, AttributeError):
                pass

        return subjects
