from bs4 import BeautifulSoup
import requests
import datetime
import re

url     = "https://www.avogadros.com/"
webPage = requests.get(url)
soup    = BeautifulSoup(webPage.text, "html.parser")

months      = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
h4sWithText = []
startIndex  = 0
defaultTime = ""
events      = []
defaultStartTime = "01:00:00-07:00"
defaultEndTime   = "03:00:00-07:00"

def extractTime(string):
    startTime   = "01:00:00-07:00"
    endTime     = "03:00:00-07:00"
    timeString = string.replace(" ", "")
    timeString = re.sub("[a-zA-Z]", "", timeString)

def extractDate(string):
    splitString = string.split(",")
    monthNumber = "0"
    dayNumber   = "0"


    for stringIndex in range(len(splitString)):
        value = splitString[stringIndex].lower()
        for i in range(len(months)):
            if months[i] not in value:
                continue
            monthNumber = str(i + 1)
            try:
                dayNumber = value.split(" ")[1]
            except IndexError(error):
                print(f'ERROR IN AVOGADROS: {value} can\'t be split into day number')
                continue
            if stringIndex >= len(splitString) - 1:
                continue
            timeString = splitString[stringIndex + 1].replace(" ", "")
            timeString = re.sub("[a-zA-Z]", "", timeString)
            print(timeString)
          

    date = "-".join((str(datetime.date.today().year), monthNumber, dayNumber))
    return date, "temp", "temp"


defaultEvent = {
            "summary": "Default Avogadro's Title",
            "description": "Default Avogadro's Description",
            "location": "605 S Mason St, Fort Collins, CO 80524",
        }

for h4Element in soup.find_all("h4"):
    if len(h4Element.get_text()) > 1:
        h4sWithText.append(h4Element)
        if h4Element.get_text() == "Shows":
            startIndex = len(h4sWithText) #when the "Shows" span element appears in the website, it's followed by an empty span, and then the first show title

eventName = ""

for i in range(startIndex, len(h4sWithText) - 1): #start at the first show, and the final span is just empty
    text = h4sWithText[i].get_text().replace("\xa0", "").strip()
    if len(text) <= 1:
        continue

    if eventName == "":
        eventName = text
        continue

    date, startTime, endTime = extractDate(text)
    # print(f'{eventName}: {date}-{startTime}')
    # print(f'{eventName}: {date}-{endTime}')
    eventName = ""