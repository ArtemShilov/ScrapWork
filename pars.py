import requests
import codecs

headers = {}
url = 'https://www.work.ua/ru/jobs-kyiv-python/'

response = requests.get(url)

handler = codecs.open('work_ua.html', 'w', 'utf-8')
handler.write(str(response.text))
handler.close()
