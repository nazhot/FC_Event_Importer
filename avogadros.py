from bs4 import BeautifulSoup
import requests
import datetime

url     = "https://www.avogadros.com/"
webPage = requests.get(url)
soup    = BeautifulSoup(webPage.text, "html.parser")

months      = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
h4sWithSpan = []
startIndex  = 0
defaultTime = ""
events      = []
defaultStartTime = "01:00:00-07:00"
defaultEndTime   = "03:00:00-07:00"

def extractDate(string):
    splitString = string.split(",")
    monthNumber = "0"
    dayNumber   = "0"
    for value in splitString:
        value = value.lower()
        for i in range(len(months)):
            if months[i] not in value:
                continue
            monthNumber = str(i + 1)
            dayNumber = value.split(" ")[1]

    date = "-".join((str(datetime.date.today().year), monthNumber, dayNumber))
    return date, "temp", "temp"


defaultEvent = {
            "summary": "Default Avogadro's Title",
            "description": "Default Avogadro's Description",
            "location": "605 S Mason St, Fort Collins, CO 80524",
        }

for h4Element in soup.find_all("h4"):
    if h4Element.span:
        h4sWithSpan.append(h4Element)
        if h4Element.span.decode_contents() == "Shows":
            startIndex = len(h4sWithSpan) + 1 #when the "Shows" span element appears in the website, it's followed by an empty span, and then the first show title

eventName = ""

for i in range(startIndex, len(h4sWithSpan) - 1): #start at the first show, and the final span is just empty
    text = h4sWithSpan[i].get_text().replace("\xa0", "").strip()
    if len(text) <= 1:
        continue

    if eventName == "":
        eventName = text
        print("empty")
        continue

    date, startTime, endTime = extractDate(text)
    print(f'{eventName}: {date}-{startTime}')
    print(f'{eventName}: {date}-{endTime}')
    eventName = ""