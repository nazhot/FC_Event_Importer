from __future__ import print_function


import magicRat
import avogadros
import comedyFort
import aggieTheatre
import maxline
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


def uploadEvents(service, eventsList, calendarId):
    calendarEvents = []
    for event in eventsList:
        if eventExists(service, event, calendarId):
            continue
        calendarEvent = service.events().insert(calendarId=calendarId, body=event).execute()

        print("Event created: " + event["summary"])
        calendarEvents.append(calendarEvent)
    return calendarEvents

def eventExists(service, event, calendarId):
    scrubbedSummary = event["summary"].replace("&amp;", "&").replace("\'", "")
    try:
        startDateTime   = datetime.datetime.fromisoformat(event["start"]["dateTime"])
    except ValueError as e:
        print(f'Invalid isoformat string for {scrubbedSummary}: {event["start"]["dateTime"]}')
        return True
    events = service.events().list(calendarId=calendarId, q=scrubbedSummary).execute()
    for existingEvent in events["items"]:
        existingStartDateTime = datetime.datetime.fromisoformat(existingEvent["start"]["dateTime"].replace("Z", "+00:00"))
        if startDateTime == existingStartDateTime:
            return True
    return False

def generateCalendarsDict(service):
    calendarDict = {}
    calendarList = service.calendarList().list().execute()
    for calendar in calendarList["items"]:
        calendarDict[calendar["summary"]] = calendar["id"]
    return calendarDict

def getCalendarId(calendarName, calendarDict, service):
    if calendarName in calendarDict:
        return calendarDict[calendarName]
    
    newCalendarObject = {
        "summary": calendarName,
        "timeZone": "America/Denver"}
    print(f'Generating new sub-calendar for {calendarName}')
    newCalendar = service.calendars().insert(body=newCalendarObject).execute()
    return newCalendar["id"]

def main():
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

        calendarDict = generateCalendarsDict(service)

        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")

        venues = [magicRat, comedyFort, avogadros, aggieTheatre, maxline]

        with webdriver.Firefox(options=options) as browser:

            for venue in venues:
                print(f'Getting {venue.name} events')
                events = venue.getEventData(browser)
                print(f'Completed, {len(events)} events found')
                calendar = getCalendarId(venue.name, calendarDict, service)
                uploadEvents(service, events, calendar)

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
