import re

defaultStartTime  = "01:00"
defaultEndTime    = "03:00"
endingOffset      =":00-06:00"
defaultEventHours = 2

#The default event, helps show if there is an issue with scraping a particular website
#Is the same across all venues other than the venue name/location
def getDefaultEvent(venueName, venueLocation):
    defaultEvent = {
            "summary": f'Default {venueName} Title',
            "description": f'Default {venueName} Description',
            "location": venueLocation,
        }
    return defaultEvent

#Converts the date elements/time into the format that expected by Google Calendar:
#   {YYYY}-{MM}-{DD}T{HH}:{MM}:00-07:00
#time parameter is expected to be H?H:MM format
def convertToEventDateTime(day, month, year, time):
    day   = str(day).rjust(2, "0")
    month = str(month).rjust(2, "0")
    year  = str(year)
    time  = str(time).rjust(5, "0")

    return f'{year}-{month}-{day}T{time}:00-06:00'

#Add the specified number of hours to the given time
#Input has to be {H?H}:{MM} format to work, if it isn't it is just returned
def addHoursToTime(timeString, hoursToAdd):
    pattern = re.compile("\d?\d:\d\d$")
    if not pattern.match(timeString):
        return timeString
    
    hour, minute = timeString.split(":")
    hour = str((int(hour) + hoursToAdd) % 24)
    return f'{hour}:{minute}'

#Convert a time that includes a meridian into the standard time format expected by Google Calendar:
#   {HH}:{MM}
#Input has to be {H?H}:{MM} {merdian}, or {H?H} {meridian}
def convertMeridianTime(timeString):
    timeString = timeString.lower()
    timeString = timeString.replace(" ", "")
    pattern1 = re.compile("\d?\d:\d\d[ap]m$")
    pattern2 = re.compile("\d?\d[ap]m$")

    if pattern2.match(timeString):
        timeString = timeString[:-2] + ":00" + timeString[-2:]

    if not pattern1.match(timeString):
        print(f'{timeString} does not match the format needed for meridian time')
        return defaultStartTime

    meridian = timeString[-2:]
    time     = timeString[:-2]
    hour, minute  = time.split(":")
    if meridian == "pm" and hour != "12":
        hour = str(int(hour) + 12)
    elif meridian == "am" and hour == "12":
        hour = "00"
    hour = hour.rjust(2, "0")
    return f'{hour}:{minute}'

def convertPMTimeWithoutMeridian(timeString):
    pattern1 = re.compile("\d?\d:\d\d$")
    pattern2 = re.compile("\d?\d$")

    if pattern2.match(timeString):
        timeString += ":00"
    
    if not pattern1.match(timeString):
        print(f'{timeString} does not match the format needed for non-meridian time')
        return defaultStartTime

    timeString += " pm"
    return convertMeridianTime(timeString)