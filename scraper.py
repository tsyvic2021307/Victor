import requests
from bs4 import BeautifulSoup

def scrape(link):
    fulllist = []
    pagenumber = 1
    done = False
    while not done:
        response = requests.get("%s?buy=buynow&page=%d" %(link, pagenumber))
        pagenumber += 1 
        soup = BeautifulSoup(response.text, "html.parser")
        totalcount = int(soup.find("span", {"id":"totalCount"}).text.strip())
        lowcount = int(soup.find("span", {"id":"lowCount"}).text.strip())
        if totalcount < lowcount:
            done = True
        else:
            itemlist = soup.findAll("a")
            fulllist += itemlist
    return fulllist           


def process(fulllist):
    goodlist = []
    for item in fulllist:
        try:
            item_title = item.find("div", {"class":"title"}).text.strip()
            item_price = item.find("div", {"class":"listingBuyNowPrice"}).text.strip()
        except:
            continue
        item_URL = "https://trademe.co.nz" + item["href"]
        # print(item_title, item_price, item_URL)
        for item in goodlist:
            if item["title"] == item_title and item["price"] == item_price:
                break
        else:
            goodlist.append({"title" : item_title, "price" : item_price, "url" : item_URL})
    return goodlist

list1 = process(scrape("https://www.trademe.co.nz/gaming/playstation-4/consoles"))
for item in list1:
    print(item["title"], item["price"], item["url"])



