# time-section
DATE_FORMAT = '%d-%m-%Y'
TIME_FORMAT = '%H:%M:%S'

SUBJECT_BODY = \
    '''
    LESSON:{lesson}
    STARTTIME:{start_time}
    ENDTIME:{end_time}
    DAY:{day}
    WEEK:{week}
    LOCATION:{auditorium}
    PROFESSOR:{professor}
    GROUP:{group}
    '''

URLS_FILE = 'groups_urls'

MAIN_URL = 'https://students.bmstu.ru'
GROUPS_LIST_URL = '/schedule/list'

DAY_MAP = {
    "ПН": "Monday",
    "ВТ": "Tuesday",
    "СР": "Wednesday",
    "ЧТ": "Thursday",
    "ПТ": "Friday",
    "СБ": "Saturday"
}
