<p align="center">
  <a href="https://noahzydel.com">
    <img alt="Noah Logo" height="128" src="./.github/resources/NoahLogo.svg">
    <h1 align="center">Noah Zydel</h1>
  </a>
</p>

---

- [📖 Overview](#-overview)
- [⭐️ Current Version](#-current-version)
- [🔜 Hopeful Features](#-hopeful-features)
- [🪚 Built With](#-built-with)
- [🔨 Build Instructions](#-build-instructions)
- [🔄 Adding Recurring Events](#-adding-recurring-events)

**This code is intended for personal use. Use of the output of this code for anything other than your own, personal Google Calendar without permission from the businesses is done at your own risk**

# Fort Collins Event Importer
A web scraper to gather upcoming events happening around Fort Collins and add them to a Google Calendar.
<p align="center">
<img src="./.github/resources/full-calendar-example.png">
</p>

## 📖 Overview
A python program used to consolidate a bunch of popular locations in Fort Collins and their events into one Google Calendar. This allows for one to tell at a glance what events are happening today, next week, next month, all within one place, and without having to navigate to and search through multiple websites. The program uses [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) web scraping in order to go through websites for Aggie Theatre, Magic Rat, Avogadro's Number, Comedy Fort (more incoming), and gather events happening in order to import into Google Calendar using their RESTful API. Events are also split into different sub-calendars, differentiated by venue, making filtering easy.

<img src="./.github/resources/subcalendar.png">

In addition, it allows for you to input recurring events on your own, to handle situations where a business gives information about the event in one blurb that is not easily scraped. 

## ⭐️ Current Version
v0.0.1
- **Venues Gathered**
  - Aggie Theatre (https://www.z2ent.com/aggie-theatre)
  - Magic Rat (https://www.theelizabethcolorado.com/magicratlivemusic)
  - Avogadro's Number (https://www.avogadros.com/)
  - Comedy Fort (https://www.comedyfortcollins.com/)
  - Maxline (https://maxlinebrewing.com/live-music/)
- Events are added to different sub-calendars, defined by venue name, for easy filtering
  - Attempting to add an event from a venue that does not currently have a sub-calendar will result in the creation of that sub-calendar
- Events already in the calendar will not be re-added
- You can define recurring events (Venue name/location, summary, description, and repeat rules) in order to add them to the different venue's sub-calendars
  
## Previous Versions
N/A

## 🔜 Hopeful Features
- Automate the adding of Gryphon Games, Wolverine Farm, and any future calendars I find that are already Google Calendars that can be imported with a link
- **Venues to Add**
  - Lyric (https://lyriccinema.com/home)
  - Washington's (https://washingtonsfoco.com/)
  - The Lincoln Center (https://www.lctix.com/)
  - Armory (https://armoryfoco.com/)
  - Bas Bleu (https://basbleu.org/)
  - Swing Station (https://www.swingstationlaporte.com/)
  - The Atrium (https://atriumfoco.com/)
  - Visit Fort Collins (https://www.visitftcollins.com/events/?locale=en-US)
  - New Belgium (https://www.newbelgium.com/visit/fort-collins/)
  - Odell Brewing (https://www.odellbrewing.com/locations/fort-collins/)
  - Cinemark (https://www.cinemark.com/theatres/co-fort-collins/cinemark-movie-bistro-and-xd?utm_medium=organic&utm_source=gmb&utm_campaign=local_listing_theater&utm_content=GMB_listing&y_source=1_MTc0OTMyMTQtNzE1LWxvY2F0aW9uLndlYnNpdGU%3D)
  - Chippers (https://www.chipperslanes.com/locations/830northfortcollins/)
  - The Mishawake (https://www.themishawaka.com/)
  
## 🪚 Built With
- python
- BeautifulSoup
- selenium
- Google Calendar RESTful API

## 🔨 Build Instructions
After forking and cloning, navigate to the repository in your command line, enter a python virtual environment, install the python libraries:
```
pip install -r requirements.txt
```
If you do not have a copy of your Google Calendar API credentials, visit [developers.google.com](https://developers.google.com/workspace/guides/create-credentials) and follow the instructions.
Add credentials.json to the project folder.
Run the following script in your command line:
```
python importer.py
```
You will be prompted to authorize the app to connect to your Google Calendar

## 🔄 Adding Recurring Events
The repository comes with a bundle of recurring events already, within [recurring.json](/recurring.json). Most of these events are Trivia and Bingo Nights. The file is an array of JSON objects, each pertaining to a different venue. If the venue is already present, skip to the next section. Otherwise, you will need to add a new JSON object to the array. Each JSON object requires 3 key-value pairs:
- `venue name`: _string_, the name of the venue, which will also be the name of the sub-calendar its events go on
- `location`:   _string_, the location of the event, copied from a Google Maps entry
- `events`:     _array_,  event JSON object(s) with the requirements listed in the next section


To add an event to an existing venue, locate the venue's `events` array. Add a JSON object element with the following requirements:
- `summary`:     _string_,      title of the event
- `description`: _string_,      description of the event
- `start`:      _JSON object_, start information of the event with the following requirements
  - `dateTime`: _string_, the date/time that the event starts, formatted according to [RFC3339](https://www.rfc-editor.org/rfc/rfc3339)
  - `timeZone`: _string_, the time zone the event takes place in, formatted as an IANA Time Zone Database name, e.g. America/Denver for these events
- `end`:      _JSON object_, end information of the event with the following requirements
  - `dateTime`: _string_, the date/time that the event ends, formatted according to [RFC3339](https://www.rfc-editor.org/rfc/rfc3339)
  - `timeZone`: _string_, the time zone the event takes place in, formatted as an IANA Time Zone Database name, e.g. America/Denver for these events

Avogadro's Number events within the given file:

<img src="./.github/resources/recurring-example.png">