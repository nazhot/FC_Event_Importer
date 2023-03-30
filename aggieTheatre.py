from bs4 import BeautifulSoup
import requests
import datetime
import re
import common
import time

def getInfoFromEventPage(soup, className):
    element = soup.find("li", class_ = className)
    if element is None:
        return None

    text = element.find("span").get_text().strip()
    return text

def getEventData():
    events = []
    url     = "https://www.z2ent.com/aggie-theatre"
    try:
        webPage = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f'Aggie\'s wasn\'t able to connect to {url}')
        exit
    soup         = BeautifulSoup(webPage.text, "html.parser")
    defaultEvent = common.getDefaultEvent("Aggie Theatre", "204 S College Ave, Fort Collins, CO 80524")
    eventElement = soup.find("div", class_ = "eventItem")

    for eventElement in soup.find_all("div", class_="eventItem"):
        eventDateElement = eventElement.find("span", class_ = "m-date__singleDate")
        eventDate        = eventDateElement.get_text().strip()[5:]
        eventNameElement = eventElement.find("h3")
        eventName        = eventNameElement.get_text().strip()
        eventDescElement = eventElement.find("h4")
        eventLinkElement = eventElement.find("a")
        eventLink        = eventLinkElement["href"]

        if eventDescElement is None:
            eventDescription = defaultEvent["description"]
        else:
            eventDescription = eventDescElement.get_text().strip()

        countTry = 0
        while countTry < 5:
            eventPage   = requests.get(eventLink)
            eventSoup   = BeautifulSoup(eventPage.text, "html.parser")
            eventStarts = getInfoFromEventPage(eventSoup, "sidebar_event_starts")
            eventPrices = getInfoFromEventPage(eventSoup, "sidebar_ticket_prices")
            if eventPrices is None:
                eventPrices = "Prices Unknown"
            
            if eventStarts is not None:
                break
            time.sleep(3)
            countTry += 1

        if eventStarts is None:
            eventStarts = common.defaultStartTime;

        eventStarts   = eventStarts.rjust(5, "0")
        startDateTime = eventDate + " " + eventStarts
        try:
            startDateTime = datetime.datetime.strptime(startDateTime, "%b %d, %Y %I:%M %p")
        except ValueError as e:
            startDateTime = datetime.datetime.strptime(startDateTime, "%B %d, %Y %I:%M %p")
        
        endDateTime              = startDateTime + datetime.timedelta(hours=common.defaultEventHours)
        eventDescription         = f'{eventDescription}\n{eventLink}\n{eventPrices}'
        eventCopy                = defaultEvent.copy()
        eventCopy["summary"]     = eventName
        eventCopy["description"] = eventDescription
        eventCopy["start"]       = {"dateTime": startDateTime.isoformat() + common.endingOffset}
        eventCopy["end"]         = {"dateTime": endDateTime.isoformat()   + common.endingOffset}

        events.append(eventCopy)

    return events