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
from scraping.models import Vacancy, City, Language, Errors

User = get_user_model()

parsers = (
    (work_ua, 'https://www.work.ua/ru/jobs-kyiv-python/'),
    (jobitt_scrap, 'https://jobitt.com/ru/job-openings?gclid=Cj0KCQjwwJuVBhCAARIsAOPwGAT3T3ntveS3nFWR8sM6k_3PSlhLiE_xazlzWcMsqzzRz92CEVTPtRUaAnROEALw_wcB&search=Python&page=1&city=265'),
    (jobs_ua, 'https://jobs.ua/vacancy/kiev/rabota-python'),
           )


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list


city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    vacancy = Vacancy(**job, city=city, language=language)
    try:
        vacancy.save()
    except DatabaseError:
        pass

if errors:
    er = Errors(data=errors).save()

# handler = codecs.open('work.txt', 'w', 'utf-8')
# handler.write(str(jobs))
# handler.close()
