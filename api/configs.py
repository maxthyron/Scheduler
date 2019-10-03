# time-section
DATE_FORMAT = '%d-%m-%Y'
API_URL = 'http://142.93.174.191/start_date/'

SUBJECT_BODY = \
    '''
    LESSON:{lesson}
    STARTTIME:{startTime}
    ENDTIME:{endTime}
    LOCATION:{auditorium}
    DESCRIPTION:{professor}
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
