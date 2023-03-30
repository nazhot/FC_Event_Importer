from bs4 import BeautifulSoup
import common
import datetime

name = "Magic Rat"

def getEventData(browser):

    events = []
    defaultEvent = common.getDefaultEvent(name, "111 Chestnut St, Fort Collins CO 80524")

    url = "https://www.theelizabethcolorado.com/magicratlivemusic#live-music"

    browser.get(url)
    html = browser.page_source

    soup = BeautifulSoup(html, "html.parser")

    for eventContainer in soup.find_all("div", class_="event-info-container"):
        bandContainer = eventContainer.find("h3")
        timeContainer = eventContainer.find("time")
        startTime     = timeContainer["datetime"].replace(" ", "T") + common.endingOffset
        endTime       = datetime.datetime.fromisoformat(startTime) + datetime.timedelta(hours=common.defaultEventHours)
        endTime       = endTime.isoformat()
        band          = bandContainer.decode_contents()
        eventCopy     = defaultEvent.copy()

        eventCopy["summary"] = band
        eventCopy["start"] = {"dateTime": startTime, "timeZone": "America/Denver",}
        eventCopy["end"]   = {"dateTime": endTime, "timeZone": "America/Denver",}

        events.append(eventCopy) 
    return events