from api.groups import unload_all_groups
from api.logger import LogMachine as log
from api.day import parse_row
import json
import requests
from api import configs
from bs4 import BeautifulSoup as bsoup

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbproject.settings")

def parse_group_week(soup):
    for dID, day in enumerate(soup.select('div.col-md-6.hidden-xs')):
        day_table = day.contents[1]
        rows = day_table.findAll('tr')
        for row in rows[2:]:
            subjects = parse_row(row.contents, dID)
            if subjects:
                for s in subjects:
                    s.save()
                    log.attn(s)


def get_one_group(url, outdir):
    page_html = requests.get(url)
    soup = bsoup(page_html.content, 'lxml')
    parse_group_week(soup)


def get_all_groups(outdir):
    log.info('Going to schedules list page')
    list_page_response = requests.get(configs.MAIN_URL + configs.GROUPS_LIST_URL)
    log.info('Parsing your group(s) url(s)')
    soup = bsoup(list_page_response.content, 'lxml')

    for valid_group_code, url in unload_all_groups(soup, outdir):
        log.info('Going to your group({}) schedule page(at {})'.format(valid_group_code, url))
        page_html = requests.get(url)

        log.info('Parsing your schedule')
        soup = bsoup(page_html.content, 'lxml')

        parse_group_week(soup)

    log.info('Done!')


def read_json(outdir):
    with open(outdir + "mapping.json", "r") as read_file:
        schedule_json = json.load(read_file)

    for group in schedule_json:
        log.info('Going to your group({}) schedule page(at {})'.format(group['group'],
                                                                       group['url']))
        page_html = requests.get(group['url'])

        log.info('Parsing your schedule')
        soup = bsoup(page_html.content, 'lxml')

        parse_group_week(soup)

    log.info('Done!')


def read_group_html(outdir):
    with open(outdir + "schedule.html", "r") as page_html:
        soup = bsoup(page_html, "lxml")
        parse_group_week(soup)
    log.info("Done!")


def main():
    # get_all_groups("/Users/thyron/Desktop/db-course/temp/")
    # read_json("/Users/thyron/Desktop/db-course/temp/")
    # read_group_html("/Users/thyron/Desktop/db-course/temp/")
    get_one_group("https://students.bmstu.ru/schedule/62f00e92-a264-11e5-be69-005056960017",
                  "/Users/thyron/Desktop/db-course/temp/")


if __name__ == "__main__":
    main()
