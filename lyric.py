from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def getEventData(browser):

    events = []

    defaultEvent = {
                "summary": "Default Lyric Title",
                "description": "Default Lyric Description",
                "location": "1209 N College Ave, Fort Collins CO 80524",
            }

    url = "https://lyriccinema.com/upcoming"

    browser.get(url)
    print(browser.prettify())
    delay = 10
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "row group-section")))
    except TimeoutException:
        browser.quit()
        print("Took too long to load")
        return
    html = browser.page_source

    soup = BeautifulSoup(html, "html.parser")

    for eventContainer in soup.find_all("div", class_="row group-section"):
        event = defaultEvent.copy()
        dayOfWeek = event.find_element(By.CLASS_NAME,"text-subtitle1").decode_contents()

        print(dayOfWeek)

        #print(eventContainer.prettify())




if __name__ == "__main__":
    from selenium import webdriver
    options = webdriver.FirefoxOptions()
    #options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    getEventData(browser)
    browser.quit()
