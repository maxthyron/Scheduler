import json
import sys

from api.logger import LogMachine as log
from api import configs


def group_code_formatter(group_url):
    try:
        stripped_url = group_url.text.lstrip()[:11].rstrip()
        return stripped_url
    except AttributeError:
        log.error('There is no schedule for the group specified.')


def unload_all_groups(soup):
    all_urls = soup.find_all('a', 'btn btn-sm btn-default text-nowrap')
    urls_count = len(all_urls)

    mapping = []
    for url_id, group_url_button in enumerate(all_urls):
        try:
            valid_group_code = group_code_formatter(group_url_button)
            log.info('Processing {} | {}/{} | [{}%]'.format(
                valid_group_code,
                url_id + 1,
                urls_count,
                round((url_id + 1) / urls_count * 100, 2)
                ))

            url = configs.MAIN_URL + group_url_button['href']

            yield (
                valid_group_code,
                url,
                )

            mapping.append({
                "group": valid_group_code,
                "url":   url
                })
        except Exception as e:
            log.error((e, url_id, group_url_button))
