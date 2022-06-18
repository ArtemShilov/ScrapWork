import asyncio
import codecs
import os
import sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ScrapWork.settings'

import django
django.setup()
from django.db import DatabaseError

from scraping.pars import *
from scraping.models import Vacancy, City, Language, Errors, Url

User = get_user_model()

parsers = (
    (work_ua, 'work'),
    (jobitt_scrap, 'rabota'),
    (jobs_ua, 'jobs'),
           )


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dict[pair]
        urls.append(tmp)
    return urls


# city = City.objects.filter(slug='kiev').first()
# language = Language.objects.filter(slug='python').first()

jobs, errors = [], []


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)


settings = get_settings()
url_list = get_urls(settings)
loop = asyncio.get_event_loop()

tmp_task = [
            (func, data.get(key), data['city'], data['language'])
            for data in url_list
            for func, key in parsers
            ]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_task])

for data in url_list:

    for func, key in parsers:
        url = data['url_data'][key]
        j, e = func(url, city=data['city'], language=data['language'])
        jobs += j
        errors += e

for job in jobs:
    vacancy = Vacancy(**job)
    try:
        vacancy.save()
    except DatabaseError:
        pass

if errors:
    er = Errors(data=errors).save()

# handler = codecs.open('work.txt', 'w', 'utf-8')
# handler.write(str(jobs))
# handler.close()
