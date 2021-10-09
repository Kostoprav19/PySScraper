import sys

import requests
import smtplib
import ssl
from bs4 import BeautifulSoup
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def filter_flats(item):
    if item['rooms'] >= 3 \
            and (item['type'] == 'Jaun.' or item['type'] == 'Specpr.') \
            and not 'Kaivas 50' in item['street'] \
            and item['m2'] > 70:
        return True
    else:
        return False

def getList(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    firstElements = soup.find_all(class_='am')
    otherElements = soup.find_all(class_='msga2-o pp6')
    list = [{} for sub in range(len(firstElements))]
    elCount = 7

    for i in range(len(firstElements)):
        list[i]['text'] = firstElements[i].getText()
        list[i]['href'] = "https://ss.lv/" + firstElements[i].get('href')
        list[i]['street'] = otherElements[i * elCount].getText()
        list[i]['rooms'] = int(otherElements[i * elCount + 1].getText())
        list[i]['m2'] = int(otherElements[i * elCount + 2].getText())
        list[i]['floor'] = otherElements[i * elCount + 3].getText()
        list[i]['type'] = otherElements[i * elCount + 4].getText()
        list[i]['pricem2'] = otherElements[i * elCount + 5].getText()
        list[i]['price'] = otherElements[i * elCount + 6].getText()

    return list

def formatTable(myList):
    html = """
    <html><body>
    <p>Look:</p>
    {table}
    </body></html>
    """
    html = html.format(table=tabulate(myList, headers="keys", tablefmt="html"))

    return html

def sendEmail(name, text):
    smtp_server = "smtp.gmail.com"
    port = 465  # For SSL
    password = "myPassword"
    email = "myemail@example.com"

    message = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(text, 'html')])
    message['Subject'] = "Today's hot deals " + name
    message['From'] = "PySScrapper"
    message['To'] = email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(email, password)
        server.send_message(message)

sections =[
  {
    "name":   "Mežciems",
    "url":    "https://www.ss.lv/lv/real-estate/flats/riga/mezhciems/sell/",
    "filter": "filter_flats"
  },
  {
    "name":   "Jugla",
    "url":    "https://www.ss.lv/lv/real-estate/flats/riga/yugla/sell/",
    "filter": "filter_flats"
  },
  {
    "name":   "Purvciems",
    "url":    "https://www.ss.lv/lv/real-estate/flats/riga/purvciems/sell/",
    "filter": "filter_flats"
  }
]
thismodule = sys.modules[__name__]

for item in sections:
    myFilter = getattr(thismodule, item["filter"])
    myList = list(filter(myFilter, getList(item["url"])))
    sendEmail(item["name"], formatTable(myList))
