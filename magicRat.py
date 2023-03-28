from bs4 import BeautifulSoup


def getEventData(browser):

    events = []

    defaultEvent = {
                "summary": "Default Magic Rat Title",
                "description": "Default Magic Rat Description",
                "location": "111 Chestnut St, Fort Collins CO 80524",
            }

    url = "https://www.theelizabethcolorado.com/magicratlivemusic#live-music"

    browser.get(url)
    html = browser.page_source

    soup = BeautifulSoup(html, "html.parser")
    
    #print(soup.prettify())

    for eventContainer in soup.find_all("div", class_="event-info-container"):
        bandContainer = eventContainer.find("h3")
        timeContainer = eventContainer.find("time")

        startTime = timeContainer["datetime"].replace(" ", "T") + "-06:00"
        startHour = startTime.split("T")[1].split(":")[0]
        endHour   = str((int(startHour)  + 2) % 24) + ":00"
        endTime = startTime.replace(startHour + ":00", endHour)
        band = bandContainer.decode_contents()
        
        eventCopy = defaultEvent.copy()

        # print(startTime)
        # print(endTime)
        eventCopy["summary"] = band
        eventCopy["start"] = {"dateTime": startTime}
        eventCopy["end"]   = {"dateTime": endTime}
        #print(time)
        #print(band)

        #print(eventCopy)
        events.append(eventCopy) 
    return events