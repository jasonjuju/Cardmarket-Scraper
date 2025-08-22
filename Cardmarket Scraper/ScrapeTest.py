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


#**If price trend is lower than available from, then it can be got cheaper**

class CardResults:
    def __init__(self, name, driver):
        self.name = name
        self.RetrieveSellers(driver)

        nameList = driver.find_elements(By.CSS_SELECTOR, "span.d-flex.has-content-centered.me-1 > a")
        priceList = driver.find_elements(By.CSS_SELECTOR, "span.color-primary.small.text-end.text-nowrap.fw-bold")

        self.sellers = []
        self.prices = []

        self.lowestPrice = None


        for i in range(len(nameList)):
            if nameList[i].text not in self.sellers:
                

                #0,15 € price format
                retrievedPrice = priceList[2*i + 1].text
                
                formattedPrice = re.sub(r"[€ ]", "", retrievedPrice)
                formattedPrice = re.sub(r",", ".", formattedPrice)
                formattedPrice = float(formattedPrice)

                if self.lowestPrice == None:
                    self.lowestPrice = formattedPrice

                #If price is higher than £1.15 more than cheapest, break out of loop
                if formattedPrice >= self.lowestPrice + 1.15:
                    break

                self.sellers.append(nameList[i].text)
                self.prices.append(formattedPrice)

    def RetrieveSellers(self, driver):
        driver.get(self.GetURL())
        
        #get results for card

    def GetURL(self):
        url = "https://www.cardmarket.com/en/Magic/Cards/" + self.name +"?sellerCountry=" + str(country) +"&language=" + str(language)
        return url

class CardSeller:
    def __init__(self, name):
        self.name = name

        self.cards = []
    
    def AddCard(self, cardName, price):
        self.cards.append(Card(cardName, price))
    
class Card:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def GetCardName(self):
        return self.name
    
    def GetCardPrice(self):
        return self.price
    

def CalculateLeastSellers(allSellers):

    mostCards = 0
    highestSeller = None

    for sel in allSellers:
        if len(sel.cards) > mostCards:
            mostCards = len(sel.cards)
            highestSeller = sel
    
    print("Seller with most cards: ", highestSeller.name)

    for c in highestSeller.cards:
        print("Card: ", c.name, " Price: ", c.price)

if __name__ == "__main__":


    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())




    # Initialize driver properly
    driver = webdriver.Chrome(service=service, options=options)

    CardsResultList = []

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

            CardsResultList.append(CardTest)


            
    totalPrice = 0.0

    print("Results:")

    sellerList = []
    currentSellers = []

    for CardResult in CardsResultList:
        #Get owners of card
        #if owner doesn't exist, create seller and say they have that card
        #else add that card to it's corresponding seller

        for i in range(len(CardResult.sellers)):
            if CardResult.sellers[i] not in sellerList:
                newSeller = CardSeller(CardResult.sellers[i])
                newSeller.AddCard(CardResult.name, CardResult.prices[i])
                currentSellers.append(newSeller)
                sellerList.append(CardResult.sellers[i])
            else:
                for sel in currentSellers:
                    if sel.name == CardResult.sellers[i]:
                        sel.AddCard(CardResult.name, CardResult.prices[i])




        if len(CardResult.sellers) > 0:
            print(CardResult.name, ": ", CardResult.sellers[0], ": ", CardResult.prices[0])
            totalPrice += float(CardResult.prices[0])

    print("Total Price: ", totalPrice)

    #for sel in currentSellers:
    #    print("Seller: ", sel.name, " No. Cards: ", len(sel.cards))

    CalculateLeastSellers(currentSellers)

    #driver.get(TestCard.GetURL())
    #time.sleep(2)

    

    driver.quit()


    #for i in range(5):
    #    print(i+1, ": ",TestCard.sellers[i], " ", TestCard.prices[i])


