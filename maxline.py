from bs4 import BeautifulSoup
import datetime
import common

name = "Maxline Brewing"

def getEventData(_):
    defaultThursTime = "18:30"
    defaultSunTime   = "15:00"

    events       = []
    defaultEvent = common.getDefaultEvent(name, "2724 McClelland Dr #190, Fort Collins, CO 80525")
    url          = "https://maxlinebrewing.com/live-music/"
    webPage      = common.requestsGet(url, 5)
    if webPage is None:
        return []
    
    soup = BeautifulSoup(webPage.text, "html.parser")
    eventBodyElement = soup.find("tbody")

    for eventElement in eventBodyElement.find_all("tr"):
        eventInfoList        = eventElement.find_all("td")
        eventDateElement     = eventInfoList[0]
        eventBandNameElement = eventInfoList[1]
        eventBandLinkElement = eventInfoList[2]
        eventBandName        = eventBandNameElement.get_text()

        if eventBandName == "":
            continue
        
        eventDateString     = eventDateElement.get_text()
        eventBandLink       = eventBandLinkElement.get_text()
        if eventDateString.count(" ") != 1:
            print(f'Date in Maxline does not contain 1 space: {eventDateString}. Event: {eventBandName}')
            continue

        eventDay, eventDate = eventDateString.split(" ")
        startDateTime = ""
        endDateTime = ""

        eventCopy                = defaultEvent.copy()
        eventCopy["summary"]     = eventBandName
        eventCopy["description"] = eventBandLink
        eventCopy["start"]       = {"dateTime": startDateTime}
        eventCopy["end"]         = {"dateTime": endDateTime}

        events.append(eventCopy)

    return events

getEventData("")