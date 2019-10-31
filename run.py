from api.groups import unload_all_groups
from api.logger import LogMachine as log
from api.day import parse_row, create_schedule_timetable, create_schedule_timetable_csv
import json
import requests
from api import configs
from bs4 import BeautifulSoup as bsoup


def parse_group_week(soup, valid_group_code):
    subjects = []
    for dID, day in enumerate(soup.select('div.col-md-6.hidden-xs')):
        day_table = day.contents[1]
        rows = day_table.findAll('tr')
        for row in rows[2:]:
            current_subjects = parse_row(row.contents, dID, valid_group_code)
            if current_subjects:
                subjects += current_subjects
    return subjects


def read_group_html(outdir):
    with open(outdir + "schedule.html", "r") as page_html:
        soup = bsoup(page_html, "lxml")
        return parse_group_week(soup, 'HTML Import')


def get_one_group(url, valid_group_code):
    page_html = requests.get(url)
    soup = bsoup(page_html.content, 'lxml')
    return parse_group_week(soup, valid_group_code)


def get_all_groups(silent=False):
    list_page_response = requests.get(configs.MAIN_URL + configs.GROUPS_LIST_URL)
    if not silent:
        log.info('Going to schedules list page and parsing you group url')

    soup = bsoup(list_page_response.content, 'lxml')

    subjects = []
    for valid_group_code, url in unload_all_groups(soup):
        if not silent:
            log.info('Going to your group({}) schedule page'.format(valid_group_code))
        subjects += get_one_group(url, valid_group_code)
    return subjects


def read_json(outdir):
    with open(outdir + configs.URLS_FILE, "r") as read_file:
        schedule_json = json.load(read_file)

    subjects = []
    for group in schedule_json:
        log.info('Going to your group({}) schedule page'.format(group['group']))
        subjects += get_one_group(group['url'])
    return subjects


def main():
    create_schedule_timetable_csv('api/src/')
    get_all_groups()
    log.info('Done!')


if __name__ == "__main__":
    main()
