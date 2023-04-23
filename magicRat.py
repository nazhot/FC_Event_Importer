from bs4 import BeautifulSoup
import common
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

name = "Magic Rat"

def getEventData(browser):

    events = []
    defaultEvent = common.getDefaultEvent(name, "111 Chestnut St, Fort Collins CO 80524")

    #url = "https://www.theelizabethcolorado.com/magicratlivemusic#live-music"
    url = "https://www.theelizabethcolorado.com/magicratlivemusic/calendar-page"

    browser.get(url)
    # cookieAcceptButton = browser.find_element(By.ID, "truste-consent-button")
    # cookieAcceptButton.click()
    # for i in range(5):
    #     try:
    #         loadMoreButton = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "calendar-load-more")))
    #         print(loadMoreButton.text)
    #         #browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         loadMoreButton.click()
    #         #browser.execute_script("arguments[0].click();", loadMoreButton)
    #     finally:
    #         browser.quit()
    html = browser.page_source

    soup = BeautifulSoup(html, "html.parser")


  


    for eventContainer in soup.find_all("div", class_="event-info-container"):
        bandContainer = eventContainer.find("h3")
        timeContainer = eventContainer.find("time")
        startTime     = timeContainer["datetime"].replace(" ", "T") + common.endingOffset
        try:
            endTime       = datetime.datetime.fromisoformat(startTime) + datetime.timedelta(hours=common.defaultEventHours)
        except ValueError as e:
            print(f'Issue with time, {startTime}')
            continue
        endTime       = endTime.isoformat()
        band          = bandContainer.decode_contents()
        eventCopy     = defaultEvent.copy()

        eventCopy["summary"] = band
        eventCopy["start"] = {"dateTime": startTime, "timeZone": "America/Denver",}
        eventCopy["end"]   = {"dateTime": endTime, "timeZone": "America/Denver",}

        events.append(eventCopy) 
    return events
