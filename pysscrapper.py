import requests
from bs4 import BeautifulSoup


def createList(uls):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    firstElements = soup.find_all(class_='am')
    otherElements = soup.find_all(class_='msga2-o pp6')
     test = soup.find_all(class_='msg2')
    # print(*test, sep = "\n")
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


url = 'https://www.ss.lv/lv/real-estate/flats/riga/mezhciems/sell/'
list = createList(url)
# print(len(list))
print(*list, sep="\n")
