import re
from django.http import HttpResponse
import requests
from astra.config import api
import base64


def send_excursion(name, company, phone, email, message, file, url):
    name = re.sub('<[^<]+?>', '', name)
    company = re.sub('<[^<]+?>', '', company)
    phone = re.sub('<[^<]+?>', '', phone)
    email = re.sub('<[^<]+?>', '', email)
    message = re.sub('<[^<]+?>', '', message)
    url = re.sub('<[^<]+?>', '', url)

    body = f'<p>ФИО: {name}</p><p>Компания: {company}</p><p>Телефон: <a href="tel:{phone}">{phone}</a></p><p>Электронная почта: <a href="mailto:{email}">{email}</a></p><p>Вопрос: {message}</p><p>Адрес отправки: {url}</p>'

    topic = 'Сообщение с сайта astra-t.com'

    if file:
        base64_file = base64.b64encode(file.read())
        file_json = '&attachments=[{"name": "' + file.name + '", "filebody": "' + str(base64_file) + '"}]'
    else:
        file_json = ''
    
    if not 'www.' in message and not 'https://' in message and not '.com' in message and not '_' in name and len(message) < 1000:

        req = api + '&message=' + body + '&subject=' + topic + '&headers={"Reply-To":"' + name + ' <' + email + '>"}' + file_json
        x = requests.post(req)
    
        if x.status_code == 200:
            return HttpResponse('Вы успешно отправили форму...')