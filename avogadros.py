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

def convertTime(timeString):
    endingString = ":00-07:00"

    if "$" in timeString:
        timeString = timeString.split("$")[0] #one of the entries didn't have a comma between time and cost, this protects against this edge case

    if len(timeString) < 3:
        timeString += ":00"
    
    if not ":" in timeString:
        print(f'{timeString} does not contain a colon')
        return defaultStartTime

    hour  = int(timeString.split(":")[0])
    hour += 12
    return str(hour) + ":" + timeString.split(":")[1] + endingString

def extractTime(string):
    endingString = ":00-07:00"
    startTime    = "01:00"
    endTime      = "03:00"
    timeString   = string.replace(" ", "")
    timeString   = re.sub("[a-zA-Z]", "", timeString)
    if "-" in timeString:
        splitTime = timeString.split("-")
        startTime = convertTime(splitTime[0])
        endTime   = convertTime(splitTime[1])
        return startTime, endTime

    startTime = convertTime(timeString)
    startHour = int(startTime.split(":")[0])
    endHour   = startHour + 2
    endTime   = str(endHour) + ":" + startTime.split(":")[1] + endingString

    return startTime, endTime

def extractDateTime(string):
    splitString = string.split(",")
    monthNumber = "0"
    dayNumber   = "0"
    startTime   = "01:00:00-07:00"
    endTime     = "03:00:00-07:00"

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
            startTime, endTime = extractTime(splitString[stringIndex + 1])
          

    date = "-".join((str(datetime.date.today().year), monthNumber, dayNumber))
    return date, startTime, endTime


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

    date, startTime, endTime = extractDateTime(text)

    eventCopy = defaultEvent.copy()
    eventCopy["summary"] = eventName + " " + date
    eventCopy["start"]   = {"dateTime": startTime, "timeZone": "America/Denver",}
    eventCopy["end"]     = {"dateTime": endTime, "timeZone": "America/Denver",}

    events.append(eventCopy)
    eventName = ""

print(events)