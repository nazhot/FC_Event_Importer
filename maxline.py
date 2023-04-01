from bs4 import BeautifulSoup
import datetime
import common
import re

name = "Maxline Brewing"

def getEventData(_):
    defaultThuTime    = "18:30"
    defaultSunTime    = "15:00"
    customTimePattern = re.compile(".*\(.*-.*\).*") #pattern to see if there is a custom time in the event title

    events       = []
    defaultEvent = common.getDefaultEvent(name, "2724 McClelland Dr #190, Fort Collins, CO 80525")
    url          = "https://maxlinebrewing.com/live-music/"
    webPage      = common.requestsGet(url, 5)
    if webPage is None:
        return []
    
    soup = BeautifulSoup(webPage.text, "html.parser")
    eventBodyElement = soup.find("tbody")

    for eventElement in eventBodyElement.find_all("tr"):
        eventInfoList        = eventElement.find_all("td") #everything is in td's, need to just use indexes
        eventDateElement     = eventInfoList[0]
        eventBandNameElement = eventInfoList[1]
        eventBandLinkElement = eventInfoList[2]
        eventBandName        = eventBandNameElement.get_text()

        if eventBandName == "":
            continue
        
        eventDateString     = eventDateElement.get_text() #format: {day of week (short)} {month}/{day}/{year}
        eventBandLink       = eventBandLinkElement.get_text()
        if eventDateString.count(" ") != 1:
            print(f'Date in Maxline does not contain 1 space: {eventDateString}. Event: {eventBandName}')
            continue

        eventDayOfWeek, eventDate       = eventDateString.split(" ")
        eventMonth, eventDay, eventYear = eventDate.split("/")
        eventMonth                      = eventMonth.rjust(2, "0")
        eventDay                        = eventDay.rjust(2, "0")
        eventYear                       = "20" + eventYear

        if customTimePattern.match(eventBandName): #format: ({start}-{end}pm)
            timeString         = eventBandName.split("(")[-1].split(")")[0].lower().replace("pm", "")
            startTime, endTime = timeString.split("-")
            startTime          = common.convertPMTimeWithoutMeridian(startTime)
            endTime            = common.convertPMTimeWithoutMeridian(endTime)
        elif eventDayOfWeek == "Thu":
            startTime = defaultThuTime
            endTime   = common.addHoursToTime(startTime, common.defaultEventHours)
        elif eventDayOfWeek == "Sun":
            startTime = defaultSunTime
            endTime   = common.addHoursToTime(startTime, common.defaultEventHours)
        
        startDateTime = common.convertToEventDateTime(eventDay, eventMonth, eventYear, startTime)
        endDateTime   = common.convertToEventDateTime(eventDay, eventMonth, eventYear, endTime)

        eventCopy                = defaultEvent.copy()
        eventCopy["summary"]     = eventBandName
        eventCopy["description"] = eventBandLink
        eventCopy["start"]       = {"dateTime": startDateTime}
        eventCopy["end"]         = {"dateTime": endDateTime}

        events.append(eventCopy)

    return events