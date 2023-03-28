from bs4 import BeautifulSoup
import requests
import datetime
import re
import common

months      = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def extractTime(timeString):
    timeString = timeString.strip()
    textToRemove = ["$15", "Dance Lessons"] #these are the random strings that appear in some time fields
    for text in textToRemove:
        timeString = timeString.replace(text, "")
    
    if "-" in timeString: #if - is present, there is a start to end time listed, and the start time (usually) does not have pm in it, and end time (usually) does
        startTime, endTime = timeString.split("-")
        startTime = common.convertPMTimeWithoutMeridian(startTime)
        if "pm" in endTime:
            endTime = common.convertMeridianTime(endTime)
        else:
            endTime = common.convertPMTimeWithoutMeridian(endTime)
        return startTime, endTime

    if "m" in timeString: #can grab am or pm, have yet to encounter an am though
        startTime = common.convertMeridianTime(timeString)
        endTime   = common.addHoursToTime(startTime, common.defaultEventHours)
        return startTime, endTime

    startTime = common.convertPMTimeWithoutMeridian(timeString) #if this is running, the time is just a number, assume it's PM
    endTime   = common.addHoursToTime(startTime, common.defaultEventHours)

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
        startTime = common.defaultStartTime
        endTime   = common.defaultEndTime
    else:
        startTime, endTime = extractTime(splitString[dateIndex + 1])
          
    startDateTime = common.convertToEventDateTime(dayNumber, monthNumber, year, startTime)
    endDateTime   = common.convertToEventDateTime(dayNumber, monthNumber, year, endTime)

    return startDateTime, endDateTime

def getEventData():
    url            = "https://www.avogadros.com/"
    h4Texts        = []
    foundShowStart = False 
    events         = []
    defaultEvent   = common.getDefaultEvent("Avogadro's Number", "605 S Mason St, Fort Collins, CO 80524")

    try:
        webPage = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f'Avogadro\'s wasn\'t able to connect to {url}')
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

        startDateTime, endDateTime = extractDateTime(text)

        eventCopy                = defaultEvent.copy()
        eventCopy["summary"]     = eventName
        eventCopy["start"]       = {"dateTime": startDateTime, "timeZone": "America/Denver",}
        eventCopy["end"]         = {"dateTime": endDateTime,   "timeZone": "America/Denver",}

        events.append(eventCopy)
        eventName = ""
    
    return events