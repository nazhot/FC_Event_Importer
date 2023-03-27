from bs4 import BeautifulSoup
import requests
import datetime

def getUrl(monthNumber, year):
    monthNumber = str(monthNumber)
    year  = str(year)
    return "https://www.comedyfortcollins.com/calendar?month=" + monthNumber + "&year=" + year

def convertTime(timeString):
    scrubbedTimeString = timeString.replace("(Sold Out)", "")
    soldOut            = len(timeString) != len(scrubbedTimeString)
    time, meridiem     = scrubbedTimeString.split(" ")
    if meridiem == "PM":
        minute = time.split(":")[1]
        hour   = int(time.split(":")[0])
        hour  += 12
        time   = str(hour) + ":" + minute


    return time, soldOut

def getEventData():
    events = []     

    defaultEvent = {
                "summary": "Default Comedy Fort Title",
                "description": "Default Comedy Fort Description",
                "location": "167 N College Ave, Fort Collins, CO 80524",
            }
    monthNumber = datetime.datetime.now().month
    yearNumber  = datetime.datetime.now().year
    
    for i in range(0, 12): #try to get one year of data
        if monthNumber == 13:
            monthNumber = 1
            yearNumber += 1
        
        url     = getUrl(monthNumber, yearNumber)
        webPage = requests.get(url)
        soup    = BeautifulSoup(webPage.text, "html.parser")

        for dateContainer in soup.find_all("td"):
            day = dateContainer.find(class_ = "date").decode_contents()
            if day == "":
                continue

            for eventContainer in dateContainer.find_all("div"):
                eventName = eventContainer.find("a")
                if eventName is None:
                    continue
                eventName = eventName.decode_contents()
                
                eventTimesContainer = eventContainer.find("li", class_ = "event-btn-group")
                for eventTimeContainer in eventTimesContainer.find_all("a"):
                    timeString = eventTimeContainer.get_text().strip().replace("\n", "")
                    time, soldOut = convertTime(timeString)
                    print(f'{eventName}: {monthNumber}-{day} {time}, Sold Out: {soldOut}')

        monthNumber += 1




getEventData()