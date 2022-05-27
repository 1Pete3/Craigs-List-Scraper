import tkinter
import pandas
import requests
from tkinter import *
from bs4 import BeautifulSoup


def close():
    win.destroy()


def scrape():
    url = craigslistURL.get()
    # URL of the page being scraped

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    # Find the prices of each car and the price occurs twice for each listing
    price = doc.findAll("span", {"class": "result-price"})

    # Find all occurrences of the h3 tag which gives you the number of listings on a page
    start = doc.find("span",{"class": "rangeFrom"}).text
    end = doc.find("span",{"class": "rangeTo"}).text
    totalListings = int(end)-int(start) + 1
    print("Number of listings on the page", totalListings)

    # Range in the for loop, it shows the amount of times price is listed
    endOfListing = len(price)

    # Removes $ and , from the price
    bad_chars = [',', '$']

    # Two lists created, one for storing prices with the $ and , and another without those characters
    pagePrices = []
    pagePricesFiltered = []
    listings = []

    for x in range(0, endOfListing,2):
        pagePrices.append(price[x].text)

    for y in range(0, endOfListing,2):
        carprice = price[y].text
        carprice = ''.join(i for i in carprice if not i in bad_chars)
        floatCarPrice = float(carprice)
        pagePricesFiltered.append(floatCarPrice)

    print(pagePrices)
    pagePricesFiltered.sort()
    output = ['{:.2f}'.format(elem) for elem in pagePricesFiltered]
    print(output)
    print("Least Expensive item on the page: $", output[0])
    print("Most Expensive item on the page: $", output[-1],"\n")


win = tkinter.Tk()  # creating the main window and storing the window object in 'win'
win.geometry('500x200')  # setting the size of the window
win.title('Craigslist Scraper')

label = Label(win, text='Enter a valid Craigslist URL in the for sale section')
label.pack(pady=10)


craigslistURL = Entry(win,width=50)
craigslistURL.pack(pady=10)

Button(
    win,
    text="Scrape",
    padx=10,
    pady=5,
    command=scrape
).pack(pady=5)

Button(
    win,
    text="Exit",
    padx=10,
    pady=5,
    command=close
).pack(pady=5)

win.mainloop()

