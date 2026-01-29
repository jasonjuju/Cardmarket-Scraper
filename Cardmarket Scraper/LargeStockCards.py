#Look through a list of cards
#Look for cards which Cardmarket will overprice

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from CardClasses import CardResults, CardSeller, Card
import NameExceptions


if __name__ == "__main__":


    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())




    # Initialize driver properly
    driver = webdriver.Chrome(service=service, options=options)


    # Get all Cards
    CardsResultList = []

    with open("decklist.txt") as decklist:
        for line in decklist:
            fixedLine = re.sub(" // ", "-", line)
            fixedLine = re.sub(r"[',]", "", fixedLine)
            fixedLine = re.sub(r"[0-9]", "", fixedLine)
            fixedLine= fixedLine[1:-1]
            fixedLine = re.sub(" ", "-", fixedLine)
            
            print(fixedLine)


            #Currently skipping cards with different naming conventions ****
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


