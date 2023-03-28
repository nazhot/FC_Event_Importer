from bs4 import BeautifulSoup
import requests
import datetime
import re

months      = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

defaultStartTime = "01:00:00-07:00"
defaultEndTime   = "03:00:00-07:00"

def convertTime(timeString):
    endingString = ":00-07:00"

    if "$" in timeString:
        timeString = timeString.split("$")[0] #one of the entries didn't have a comma between time and cost, this protects against this edge case

    if len(timeString) < 3:
        timeString += ":00"
    
    if not ":" in timeString:
        print(f'{timeString} does not contain a colon, Avogadro\'s Number')
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

#The date/time sections are usually in the form:
#  Month Day, Time{, Cost}
#Every one I've seen has had the full month in the date section, hence why I search through months to find the right section
#There was exactly one event that had the date in the second section, so now I check every section for the date
def extractDateTime(string):
    year        = str(datetime.date.today().year)

    splitString = string.split(",")

    breakout = False

    #find which index of the array has a month in it, and which month it is
    #python is weird so the variables storing the indexes stick around after loop breaks
    for dateIndex in range(len(splitString)): 
        dateString = splitString[dateIndex].lower()

        for monthIndex in range(len(months)):
            if months[monthIndex] in dateString:
                breakout = True
                break
        if breakout:
            break

    if not breakout:
        print(f'No month found in {string}, using default, Avogadro\'s Number')
        return year + "-1-1", defaultStartTime, defaultEndTime #default if no month is found

    monthNumber = str(monthIndex + 1)

    if " " not in dateString:
        print(f'Date does not appear in right form in {dateString}, Avogadro\'s Number')
        dayNumber = "1"
    else:
        dayNumber = dateString.split(" ")[1]
    
    if dateIndex >= len(splitString) - 1:
        print(f'Date does not have a section after it, {string}, Avogadro\'s Number')
        startTime = defaultStartTime
        endTime   = defaultEndTime
    else:
        startTime, endTime = extractTime(splitString[dateIndex + 1])
          
    date = "-".join((year, monthNumber.rjust(2, "0"), dayNumber.rjust(2, "0")))
    return date, startTime, endTime

def getEventData():
    url            = "https://www.avogadros.com/"
    h4Texts        = []
    foundShowStart = False 
    events         = []
    defaultEvent   = {
            "summary": "Default Avogadro's Title",
            "description": "Default Avogadro's Description",
            "location": "605 S Mason St, Fort Collins, CO 80524",
        }

    try:
        webPage = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f'Comedy Fort wasn\'t able to connect to {url}')
        exit
    soup    = BeautifulSoup(webPage.text, "html.parser")

    for h4Element in soup.find_all("h4"): #all event/date elements are h4's, some extras sneak in though
        h4Text = h4Element.get_text() 

        if len(h4Text) <= 1: #remove the elements that are only included for space, usually they have just a space in them
            continue
            
        if not foundShowStart: #events start after the h4 element with text "Shows"
            foundShowStart = h4Text == "Shows"
            continue

        h4Texts.append(h4Text)

    eventName = ""

    for h4Text in h4Texts:
        text = h4Text.replace("\xa0", "").strip() #remove leading/trailing white space, and \xa0 appeared at the start of one event name

        if eventName == "": #order is an element having the event name, and the next element having the date/time of that event
            eventName = text
            continue

        date, startTime, endTime = extractDateTime(text)

        eventCopy                = defaultEvent.copy()
        eventCopy["summary"]     = eventName
        eventCopy["start"]       = {"dateTime": date + "T" + startTime, "timeZone": "America/Denver",}
        eventCopy["end"]         = {"dateTime": date + "T" + endTime,   "timeZone": "America/Denver",}

        events.append(eventCopy)
        eventName = ""
    
    return events