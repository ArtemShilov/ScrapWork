from scraping.pars import *
import codecs

parsers = (
    (work_ua, 'https://www.work.ua/ru/jobs-kyiv-python/'),
    (jobitt_scrap, 'https://jobitt.com/ru/job-openings?gclid=Cj0KCQjwwJuVBhCAARIsAOPwGAT3T3ntveS3nFWR8sM6k_3PSlhLiE_xazlzWcMsqzzRz92CEVTPtRUaAnROEALw_wcB&search=Python&page=1&city=265')
           )

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

handler = codecs.open('work.txt', 'w', 'utf-8')
handler.write(str(jobs))
handler.close()
