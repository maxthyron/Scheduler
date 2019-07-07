from schedule.models import Subject


# class Subject:
#     def __init__(self, info, subject_day_index, weeks_interval, time_interval):
#         self.type, self.name, self.auditorium, self.professor = info
#         self.start_time, self.end_time = time_interval
#         self.weeks_interval = weeks_interval
#         self.day = subject_day_index
#
#     def __str__(self):
#         return textwrap.dedent(configs.SUBJECT_BODY.format(lesson='{} {}'.format(self.type or '',
#                                                                                  self.name),
#                                                            startTime=self.start_time,
#                                                            endTime=self.end_time,
#                                                            auditorium=self.auditorium or '',
#                                                            professor=self.professor or ''))


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
