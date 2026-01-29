import re
import NameExceptions

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