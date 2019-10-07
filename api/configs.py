# time-section
DATE_FORMAT = '%d-%m-%Y'
DATE_URL = 'http://142.93.174.191/start_date/'

SUBJECT_BODY = \
    '''
    LESSON:{lesson}
    STARTTIME:{startTime}
    ENDTIME:{endTime}
    DAY:{day}
    WEEK:{week}
    LOCATION:{auditorium}
    PROFESSOR:{professor}
    GROUP:{group}
    '''

URLS_FILE = 'groups_urls'

# bmstu
MAIN_URL = 'https://students.bmstu.ru'
GROUPS_LIST_URL = '/schedule/list'  # '/schedule/list'


DAY_MAP = {
    "ПН": "Monday",
    "ВТ": "Tuesday",
    "СР": "Wednesday",
    "ЧТ": "Thursday",
    "ПТ": "Friday",
    "СБ": "Saturday"
    }
