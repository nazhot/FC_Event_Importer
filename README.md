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

# Fort Collins Event Importer
A web scraper to gather upcoming events happening around Fort Collins and add them to a Google Calendar.

## 📖 Overview
A python program used to consolidate a bunch of popular locations in Fort Collins and their events into one Google Calendar. The program uses [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) web scraping in order to go through websites for Aggie Theatre, Magic Rat, Avogadro's Number, Comedy Fort (more incoming), and gather events happening in order to import into Google Calendar using their RESTful API.

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
Run the following script in your command line:
```
python importer.py
```
You will be prompted to authorize the app to connect to your Google Calendar