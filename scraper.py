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
            print("AHHHHHHHHHHHH")
            continue
        item_URL = "https://trademe.co.nz" + item["href"]
        # print(item_title, item_price, item_URL)
        for item in goodlist:
            if item[0] == item_title and item[1] == item_price:
                break
        else:
            if "ps4" in item_title.lower() or "playstation 4" in item_title.lower():
                goodlist.append([item_title, item_price, item_URL])

