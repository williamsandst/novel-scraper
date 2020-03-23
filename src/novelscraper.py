from bs4 import BeautifulSoup
import html5lib
from selenium import webdriver
    
import requests
import time
import re

import dataobject
from stringhelpers import *

PRINT_PROGRESS = True

def getParsedJavaScriptHTML(website, browser):
    """Returns the parsed javascript HTML source code for a website"""
    if PRINT_PROGRESS:
        print("Scraping website with Selenium: {}".format(website))
    
    browser.get(website)
    time.sleep(4)

    if PRINT_PROGRESS:
        print("Scraping website complete")

    return BeautifulSoup(browser.page_source, "html5lib")

def getHTML(website):
    if PRINT_PROGRESS:
        print("Scraping website for plain HTML: {}".format(website))
    
    page = requests.get(website)

    if PRINT_PROGRESS:
        print("Scraping website complete")

    return BeautifulSoup(page.content, "html5lib")

def saveToFile(string, filename):
    print("Saving to file {}...".format(filename))
    text_file = open(filename, "w")
    text_file.write(string)
    text_file.close()
    print("Saved to file {}".format(filename))


class NovelScraper:
    """Parent class to be inherited for all countries. Defines two needed functions: scrape and __init__"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "N/A (BASE CLASS)"
        self.iso_code = "N/A (BASE CLASS)"
        self.source_website = "N/A (BASE CLASS)"

    def scrape(self, browser):
        """ Template for scrape function. Returns a data object containing the cases"""
        result = dataobject.DataObject(self)
        return result

class NovelScraperNO(NovelScraper):
    """Norway Coronavirus Scraper"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Norway"
        self.iso_code = "NO"
        #Source has javascript components for cases
        self.source_website = "https://www.vg.no/spesial/2020/corona/"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getParsedJavaScriptHTML(self.source_website, browser)

        result.cases = soup.find("span", class_="absolute confirmed").contents[0]
        result.deaths = soup.find("span", class_="absolute dead").contents[0]

        return result

class NovelScraperSE(NovelScraper):
    """Sweden Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Sweden"
        self.iso_code = "SE"
        #Source has plain html for cases
        self.source_website = "https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/aktuellt-epidemiologiskt-lage/"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)

        text = soup.find("p", text=re.compile("Totalt har"))
        result.cases = int(match(text.get_text(), "Totalt har {} personer"))
        result.deaths = int(match(text.get_text(), "Nationellt har {} av fallen"))

        return result