import requests
import codecs
from bs4 import BeautifulSoup

__all_ = ('work_ua', 'jobitt_scrap')

headers = {}


def work_ua(url):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', {'id': 'pjax-job-list'})
        if main_div:
            div_lst = soup.find_all('div', attrs={'class': 'job-link'})
            for div in div_lst:
                title = div.find('h2')
                href = title.a['href']
                content = div.p.text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']

                jobs.append(
                    {
                        'title': title.text,
                        'url': domain + href,
                        'description': content,
                        'company': company
                    }
                )
        else:
            errors.append({'url': url, 'title': "Div does not exists"})

    else:
        errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def jobitt_scrap(url):
    jobs = []
    errors = []
    domain = 'https://jobitt.com'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', {'class': 'list-vacancy__content__wrapper__list-vacancy'})
        if main_div:
            div_lst = soup.find_all('div', attrs={'class': 'vacancy'})
            for div in div_lst:
                title = div.find('a')
                href = title['href']
                content = div.find('div', attrs={'class': 'vacancy-description'})
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']

                jobs.append(
                    {
                        'title': title.text,
                        'url': domain + href,
                        'description': content.text,
                        'company': company
                    }
                )
        else:
            errors.append({'url': url, 'title': "Div does not exists"})

    else:
        errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


# def dou_ua(url):
#     jobs = []
#     errors = []
#     response = requests.get(url)
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         main_div = soup.find('div', id='vacancyListId')
#         if main_div:
#             li_lst = main_div.find_all('li', attrs={'class': 'l-vacancy'})
#             for li in li_lst:
#                 title = li.find('div', attrs={'class': 'title'})
#                 href = title.a['href']
#                 cont = li.find('div', attrs={'class': 'sh-info'})
#                 content = cont.text
#                 company = 'No name'
#                 a = title.find('a', attrs={'class': 'company'})
#                 if a:
#                     company = a.text
#                 jobs.append(
#                     {
#                         'title': title.text,
#                         'url': href,
#                         'description': content,
#                         'company': company
#                     }
#                 )
#         else:
#             errors.append({'url': url, 'title': "Div does not exists"})
#
#     else:
#         errors.append({'url': url, 'title': "Page do not response"})
#
#     return jobs, errors


if __name__ == '__main__':
    # url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    # url = 'https://jobitt.com/ru/job-openings?gclid=Cj0KCQjwwJuVBhCAARIsAOPwGAT3T3ntveS3nFWR8sM6k_3PSlhLiE_xazlzWcMsqzzRz92CEVTPtRUaAnROEALw_wcB&search=Python&page=1&city=265'
    # jobs = work_ua(url)
    # jobs, errors = jobitt_scrap(url)
    # handler = codecs.open('rf.txt', 'w', 'utf-8')
    # handler.write(str(jobs))
    # handler.close()


# handler = codecs.open('work_ua.csv', 'w', 'utf-8')
# handler.write(str(jobs))
# handler.close()
    pass