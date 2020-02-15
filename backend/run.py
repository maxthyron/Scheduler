import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbproject.settings")
import django

django.setup()
from schedule.models import ScheduleSubject, Day

from bs4 import BeautifulSoup as bsoup
import json
import requests
import dotenv

from api.groups import unload_all_groups
from api.logger import LogMachine as log
from api.day import parse_row, create_schedule_timetable_csv
from api import configs
import time


def parse_group_week(soup, valid_group_code, days):
    subjects = []
    for day_object, day in zip(days, soup.select("div.col-md-6.hidden-xs")):
        day_table = day.contents[1]
        rows = day_table.findAll("tr")
        for row in rows[2:]:
            current_subjects = parse_row(row.contents, day_object, valid_group_code)
            if current_subjects:
                subjects += current_subjects
    ScheduleSubject.objects.bulk_create(subjects, ignore_conflicts=True)


def read_group_html(source_dir, days):
    with open(source_dir + "schedule.html", "r") as page_html:
        soup = bsoup(page_html, "lxml")
        parse_group_week(soup, "HTML Import", days)


def get_one_group(url, valid_group_code, days):
    page_html = requests.get(url)
    soup = bsoup(page_html.content, "lxml")
    parse_group_week(soup, valid_group_code, days)


def get_all_groups():
    list_page_response = requests.get(configs.MAIN_URL + configs.GROUPS_LIST_URL)
    log.info("Collecting groups\' urls")

    soup = bsoup(list_page_response.content, "lxml")
    days = Day.objects.all()
    for valid_group_code, url in unload_all_groups(soup):
        log.info("Getting group({}) schedule page".format(valid_group_code))
        get_one_group(url, valid_group_code, days)
        time.sleep(0.2)


def read_json(outdir):
    with open(outdir + configs.URLS_FILE, "r") as read_file:
        schedule_json = json.load(read_file)

    days = Day.objects.all().iterator()
    for group in schedule_json:
        log.info("Getting group({}) schedule page".format(group["group"]))
        get_one_group(group["url"], group["group"], days)


def main():
    project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log.verbose = os.getenv("CONF_DIR")
    dotenv_file = os.path.join(project_directory, "config", ".env")
    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)
    log.verbose = os.getenv("DEBUG")

    create_schedule_timetable_csv("api/src/")
    get_all_groups()
    log.info("Done!")


if __name__ == "__main__":
    main()
