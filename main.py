import requests
from bs4 import BeautifulSoup


class Listing:
    def __init__(self, vin, year, make, model, priceOfCar, listingDate):
        self.listingDate = listingDate
        self.priceOfCar = priceOfCar
        self.model = model
        self.make = make
        self.year = year
        self.vin = vin


# URL of the page being scraped
url = "https://hartford.craigslist.org/search/cta"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

# Find the prices of each car and the price occurs twice for each listing
price = doc.findAll("span", {"class": "result-price"})

# Find all occurrences of the h3 tag which gives you the number of listings on a page
numOfListings = doc.findAll("h3")
print("Number of listings on the page", len(numOfListings))

# Removes $ and , from the price
bad_chars = [',', '$']

# Two lists created, one for storing prices with the $ and , and another without those characters
firstPagePrices = []
firstPagePricesFiltered = []
listings = []

# range is 0 to number of listings but * 2 is necessary since the price appears twice, so it's incremented by 2 to
# avoid showing the price twice
for x in range(0, len(numOfListings) * 2, 2):
    firstPagePrices.append(price[x].text)

for y in range(0, len(numOfListings) * 2, 2):
    carprice = price[y].text
    carprice = ''.join(i for i in carprice if not i in bad_chars)
    floatCarPrice = float(carprice)
    firstPagePricesFiltered.append(floatCarPrice)

print(firstPagePrices)
print(firstPagePricesFiltered)

firstPagePricesFiltered.sort()
output = ['{:.2f}'.format(elem) for elem in firstPagePricesFiltered]
print(output)
print("Cheapest car on the page: $", output[0])
print("Most Expensive car on the page: $", output[-1])
