from bs4 import BeautifulSoup
import datetime
import common

name = "Comedy Fort"

def getUrl(monthNumber, year):
    monthNumber = str(monthNumber)
    year        = str(year)

    return f'https://www.comedyfortcollins.com/calendar?month={monthNumber}&year={year}'

def getEventData(_):
    events       = []     
    defaultEvent = common.getDefaultEvent(name, "167 N College Ave, Fort Collins, CO 80524")
    monthNumber  = datetime.datetime.now().month
    yearNumber   = datetime.datetime.now().year
    
    for i in range(0, 12): #try to get one year of data
        if monthNumber == 13:
            monthNumber = 1
            yearNumber += 1
        
        url     = getUrl(monthNumber, yearNumber)
        webPage = common.requestsGet(url, 5)
        if webPage is None:
            return []

        soup    = BeautifulSoup(webPage.text, "html.parser")

        for dateContainer in soup.find_all("td"): #all of the days are held within td elements
            day = dateContainer.find(class_ = "date").decode_contents()
            if day == "": #the calendar can also have blank days just to fill it, this skips those
                continue

            for eventContainer in dateContainer.find_all("div"): #div elements hold each different event on a given day
                eventName = eventContainer.find("a")             #first 'a' element should hold the event name
                if eventName is None:                            #this represents a calendar spot that has a date, but no events
                    continue

                eventName           = eventName.decode_contents()
                eventTimesContainer = eventContainer.find("li", class_ = "event-btn-group")

                for eventTimeContainer in eventTimesContainer.find_all("a"):
                    timeString         = eventTimeContainer.get_text().strip().replace("\n", "")
                    scrubbedTimeString = timeString.replace("(Sold Out)", "")
                    soldOut            = len(timeString) != len(scrubbedTimeString)
                    startTime          = common.convertMeridianTime(scrubbedTimeString)
                    endTime            = common.addHoursToTime(startTime, common.defaultEventHours)

                    if soldOut:
                        eventName += " (Sold Out)"
                    
                    startDateTime = common.convertToEventDateTime(day, monthNumber, yearNumber, startTime)
                    endDateTime   = common.convertToEventDateTime(day, monthNumber, yearNumber, endTime)

                    eventCopy = defaultEvent.copy()
                    eventCopy["summary"] = eventName
                    eventCopy["start"]   = {"dateTime": startDateTime, "timeZone": "America/Denver",}
                    eventCopy["end"]     = {"dateTime": endDateTime, "timeZone": "America/Denver",}
                    
                    events.append(eventCopy)

        monthNumber += 1

    return events