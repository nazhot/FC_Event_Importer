from __future__ import print_function


import magicRat
import avogadros
from selenium import webdriver


import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def uploadEvents(service, eventsList):
    calendarEvents = []
    for event in eventsList:
        if eventExists(service, event):
            continue
        print(event["summary"])
        calendarEvent = service.events().insert(calendarId="primary", body=event).execute()

        print("Event created: " + event["summary"])
        calendarEvents.append(calendarEvent)
    return calendarEvents

def eventExists(service, event):
    scrubbedSummary = event["summary"].replace("&amp;", "&").replace("\'", "")
    events = service.events().list(calendarId='primary', q=scrubbedSummary).execute()
    return len(events["items"]) > 0

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)
        print("Getting Magic Rat events")
        magicRatEvents = magicRat.getEventData(browser)
        print("Completed, " + str(len(magicRatEvents)) + " events found")
        uploadEvents(service, magicRatEvents)

        print("Getting Avo's events")
        avoEvents = avogadros.getEventData()
        print("Completed, " + str(len(avoEvents)) + " events found")
        uploadEvents(service, avoEvents)
        browser.quit()


    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
