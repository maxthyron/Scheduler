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

# bmstu
MAIN_URL = 'http://web.archive.org/web/20170926061533/https://students.bmstu.ru'
GROUPS_LIST_URL = '/schedule/62f00e92-a264-11e5-be69-005056960017'  # '/schedule/list'

# physical culture
PC_LESSON_KEYREGEX = r'.*(спорту|Физ воспитание).*'
