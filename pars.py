import requests
import codecs
from bs4 import BeautifulSoup

headers = {}
domain = 'https://www.work.ua'
url = 'https://www.work.ua/ru/jobs-kyiv-python/'

response = requests.get(url)
jobs = []
errors = []
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
# handler = codecs.open('work_ua.html', 'w', 'utf-8')
# handler.write(str(response.text))
# handler.close()

# handler = codecs.open('work_ua.csv', 'w', 'utf-8')
# handler.write(str(jobs))
# handler.close()
