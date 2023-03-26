from bs4 import BeautifulSoup
import requests
import datetime

def getUrl(month, year):
    month = str(month)
    year  = str(month)
    return "https://www.comedyfortcollins.com/calendar?month=" + month + "&year=" + year

