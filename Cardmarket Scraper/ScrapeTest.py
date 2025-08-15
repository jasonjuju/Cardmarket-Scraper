#Dependencies
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from lxml import html
import time
import re
import NameExceptions

#Scraping test

#Get url of site
#https://www.cardmarket.com/en/Magic
#https://www.cardmarket.com/en/Magic/Cards/Umbral-Collar-Zealot?sellerCountry=13

# Load the URL

country = 13 # UK
language = 1 # English


#Set settings so that only uk version of cards

#get list of all cards in a reasonable format

#print them out

#synergy


class CardResults:
    def __init__(self, name, driver):
        self.name = name
        self.RetrieveSellers(driver)

        nameList = driver.find_elements(By.CSS_SELECTOR, "span.d-flex.has-content-centered.me-1 > a")
        priceList = driver.find_elements(By.CSS_SELECTOR, "span.color-primary.small.text-end.text-nowrap.fw-bold")

        self.sellers = []
        self.prices = []


        for i in range(len(nameList)):
            self.sellers.append(nameList[i].text)
            self.prices.append(priceList[2*i + 1].text)

    def RetrieveSellers(self, driver):
        driver.get(self.GetURL())
        
        #get results for card

    def GetURL(self):
        url = "https://www.cardmarket.com/en/Magic/Cards/" + self.name +"?sellerCountry=" + str(country) +"&language=" + str(language)
        return url




if __name__ == "__main__":


    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())




    # Initialize driver properly
    driver = webdriver.Chrome(service=service, options=options)

    CardsTestList = []

    with open("decklist.txt") as decklist:
        for line in decklist:
            fixedLine = re.sub(" // ", "-", line)
            fixedLine = re.sub(r"[',]", "", fixedLine)
            fixedLine = re.sub(r"[0-9]", "", fixedLine)
            fixedLine= fixedLine[1:-1]
            fixedLine = re.sub(" ", "-", fixedLine)
            
            print(fixedLine)


            #Currently skipping cards with different naming conventions
            if fixedLine in NameExceptions.exceptions:
                continue
            
            CardTest = CardResults(fixedLine, driver)

            CardsTestList.append(CardTest)


            


    print("Results:")

    for Card in CardsTestList:
        print(Card.name, ": ", Card.sellers[0], ": ", Card.prices[0])

    #TestCard = CardResults("Umbral-Collar-Zealot", driver)
    #TestCard2 = CardResults("The-Gaffer", driver)

    #driver.get(TestCard.GetURL())
    #time.sleep(2)

    

    driver.quit()


    #for i in range(5):
    #    print(i+1, ": ",TestCard.sellers[i], " ", TestCard.prices[i])


