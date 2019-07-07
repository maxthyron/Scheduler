from api.groups import unload_all_groups
from api.logger import LogMachine as log
from api.day import parse_row, create_schedule_time
import json
import requests
from api import configs
from bs4 import BeautifulSoup as bsoup


def parse_group_week(soup):
    subjects = []
    for dID, day in enumerate(soup.select('div.col-md-6.hidden-xs')):
        day_table = day.contents[1]
        rows = day_table.findAll('tr')
        for row in rows[2:]:
            current_subjects = parse_row(row.contents, dID)
            if current_subjects:
                subjects += current_subjects
                for s in current_subjects:
                    log.info(s)
    return subjects


def read_group_html(outdir):
    with open(outdir + "schedule.html", "r") as page_html:
        soup = bsoup(page_html, "lxml")
        return parse_group_week(soup)


def get_one_group(url):
    page_html = requests.get(url)
    soup = bsoup(page_html.content, 'lxml')
    return parse_group_week(soup)


def get_all_groups(outdir):
    log.info('Going to schedules list page')
    list_page_response = requests.get(configs.MAIN_URL + configs.GROUPS_LIST_URL)
    log.info('Parsing your group(s) url(s)')
    soup = bsoup(list_page_response.content, 'lxml')

    subjects = []
    for valid_group_code, url in unload_all_groups(soup, outdir):
        log.info('Going to your group({}) schedule page'.format(valid_group_code))
        subjects += get_one_group(url)
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
    # create_schedule_time("src/")
    # get_all_groups("/Users/thyron/Desktop/db-course/src/")
    # read_json("/Users/thyron/Desktop/db-course/src/")

    # get_one_group("https://students.bmstu.ru/schedule/62f00e92-a264-11e5-be69-005056960017")
    #
    subjects = read_group_html("./src/")
    for s in subjects:
        s.save()
    log.info('Done!')


if __name__ == "__main__":
    main()
