from __future__ import print_function

import magicRat
import avogadros
import comedyFort
import aggieTheatre
import maxline
import common

from selenium import webdriver
import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

#Upload recurring events defined in recurring.json
def uploadRecurringEvents(service, calendarDict):
    with open("recurring.json") as f:
        recurringEventsJSON = json.load(f)
        for venueObject in recurringEventsJSON:
            venueName     = venueObject["venue name"]
            calendarId    = getCalendarId(venueName, calendarDict, service)
            venueLocation = venueObject["location"]
            for recurringEvent in venueObject["events"]:
                eventObject             = recurringEvent
                eventObject["location"] = venueLocation
                if eventExists(service, eventObject, calendarId):
                    continue
                calendarEvent = service.events().insert(calendarId=calendarId, body=eventObject).execute()
                print(f'Recurring event created: {calendarEvent["summary"]}')

def uploadEvents(service, eventsList, calendarId):
    calendarEvents = []
    for event in eventsList:
        if eventExists(service, event, calendarId):
            continue
        calendarEvent = service.events().insert(calendarId=calendarId, body=event).execute()

        print("Event created: " + event["summary"])
        calendarEvents.append(calendarEvent)
    return calendarEvents

def eventVerifier(event):
    keysToCheck = {
        "summary": {
            "error": "No Summary",
            "value": "Default Title"
        },
        "description": {
            "error": "No Description",
            "value": "Default Description"
        },
        "start":{
            "error": "No Start Time"
        },
        "end": {
            "error" : "No End Time"
        }
    }
    errors = []
    for key in keysToCheck:
        if key in event:
            continue

        if "value" not in keysToCheck[key]:
            print(f'{key} not found in event: {event}')
            return None
        
        event[key] = keysToCheck[key]["value"]
        errors.append(keysToCheck[key]["error"])
        
    if "dateTime" not in event["start"]:
        print("No dateTime within start")
        for error in errors:
            print(error)
        print(event)
        return None

    startTime = event["start"]["dateTime"]
    try:
        startTime = datetime.datetime().fromisoformat(startTime)
    except ValueError as e:
        print("dateTime within start not formatted correctly")
        for error in errors:
            print(error)
        print(event)
        return None

    if "dateTime" not in event["end"]:
        errors.append("No dateTime within end, adding default eventTime to start")
        endTime                  = startTime + datetime.timedelta(hours=common.defaultEventHours)
        event["end"]["dateTime"] = endTime.isoformat()
        return event
    
    endTime = event["end"]["dateTime"]
    try:
        datetime.datetime().fromisoformat(endTime)
    except ValueError as e:
        print("dateTime within end not formatted correctly, adding default eventTime to start")
        endTime                  = startTime + datetime.timedelta(hours=common.defaultEventHours)
        event["end"]["dateTime"] = endTime.isoformat()

    return event

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

        #uploadRecurringEvents(service, calendarDict)
        #return

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
