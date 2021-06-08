# vinyl_webscraper_urllist.py
#
# Author: Jack Munday
#
# Webscraper implimentation using selenium and BeautifulSoup to automate the price checking of records in my amazon wishlist. Input file "urls.txt" should be a list of amazon urls with one url per line. Script then cyclesthrough all urls and get the current artist name, record title and price. Through comparing this price to the  current output data file "recpods.csv" it keeps track of the best price and calculates any % price changes.


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def records_wishlist_scraper(driver, url):
    """
    Webscraper to scrape the Artist Name, Record Title and Current Price for a given record as listed on Amazon
    specified by the url.

    params:
    ---------------------------------------------------------------------------------------------------------
    driver:         Selenium instance of the driver for the browser being used to perform the webscraping
                    e.g. driver = webdriver.Safari()
    url:            Amazon url for a given record whose price you would like to keep track of

    returns:
    ---------------------------------------------------------------------------------------------------------
    artist_name:    Name of artist for the record specified by the input url
    record_name:    Title of record for the input url
    price:          Current price of record_title
    """

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    artist = soup.find('span', attrs={'class': 'author notFaded'}).get_text()
    artist_name  = str(artist.split('\n')[1])

    record_name = soup.find('title').get_text()
    # It is quite common for amazon to add [VINYL] to the title of records, if this is the case.
    if "[VINYL]" in record_name:
        record_name, _ = record_name.split(' [VINYL]')

    # Remove artist name from title for incorrectly listed records
    if artist[indx] in record_name:
        record_name = record_name.strip(artist[indx])
        if not record_name:
            record_name = "Self Titled"

    price = soup.find('span', id="price_inside_buybox")
    
    if price is not None:
        price = price.get_text()
        price = price.strip('\n')
        price = float(price.strip('£'))

    return [artist_name, record_name, price]

##################################################################
# USING CHROME INSTEAD OF SAFARI
##################################################################
#from selenium.webdriver.chrome.options import Options
#import chromedriver_binary

# To use chrome instead import the above libraries and download the chromedriver file for your os
# below provides some options that you may want to consider using, headless is a particularly useful
# one as it runs the browers without a gui.

#chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox")
#driver = webdriver.Chrome(executable_path='/Users/jcmunday/Documents/Computing/webscraper/chromedriver', options=chrome_options)

#uncomment below if you decide to run in chrome
driver = webdriver.Safari()

# Import list of amazon url for records in wishlist and convert to a python list
url_list = open("../input_data/urls.txt", "r")
content = url_list.read()
urls = content.splitlines()

##################################################################
# INTIALISING DATA STORAGE
##################################################################
# Intialise a series of blank arrays of size urls.txt to store results in as we iterate through all records

size = len(urls)
title = [0 for _ in range(size)]
artist = [0 for _ in range(size)]
current_price = [0 for _ in range(size)]
price_change = [0 for _ in range(size)]
best_price = [0 for _ in range(size)]
previous_price = [0 for _ in range(size)]

try:
    records_df = pd.read_csv('records.csv')
    best_price = records_df['Best Price'].tolist()
    previous_price = records_df['Current Price'].tolist()
    assert len(best_price) == len(title), "Mismatched number of records in url.txt to that stored in records.csv"
except:
    best_price = [0 for _ in range(size)]
    previous_price = [0 for _ in range(size)]

print("\n>>> Fetching Record Prices")
##################################################################
# SCRAPPING DATA
##################################################################
for indx, url in enumerate(urls):
   # driver.get(url)
   # soup = BeautifulSoup(driver.page_source, features="html.parser")

   # artist_tmp = soup.find('span', attrs={'class': 'author notFaded'}).get_text()
   # artist_tmp  = artist_tmp.split('\n')
   # if type(artist_tmp[1])==str:
   #     artist[indx] = artist_tmp[1]

   # name = soup.find('title').get_text()
   # if "[VINYL]" in name:
   #     name, _ = name.split(' [VINYL]')
   # if artist[indx] in name:
   #     name = name.strip(artist[indx])
   #     if not name:
   #         name = "Self Titled"
   # title[indx] = name

   # price = soup.find('span', id="price_inside_buybox")

    #TODO: ADJUST TO INCLUDE FUNCTIONAL WEBSCRAPER DEFINED ABOVE, THIS WILL IMPROVE CLARITY OF WHAT IS GOING ON HERE
    #TODO: ADD ANOTHER SECTION TO CODE THAT WOULD KEEP TRACK OF THE HISTORICAL DATA FOR ALL RECORDS IN WISHLIST
    
   # if price is not None:
   #     price = price.get_text()
   #     price = price.strip('\n')
   #     price = float(price.strip('£'))

        artist_name, record_name, price = records_wishlist_scraper(driver, url)

        artist[indx] = artist_name
        title[indx] = record_name
        current_price[indx] = price

        if previous_price[indx] == 0:
            price_change[indx] = 0

        if best_price[indx] == 0:
            best_price[indx] = price

        if price < previous_price[indx]:
            price_change[indx] = -100*(previous_price[indx] - price) / price
            if price < best_price[indx]:
                best_price[indx] == price

        #if price == current_price:
        #    price_change[indx] = 0

        if price >= previous_price[indx] and previous_price[indx] != 0:
            price_change[indx] = 100*(price - previous_price[indx]) / previous_price[indx]

driver.quit()
price_change = [str(round(elem, 1)) for elem in price_change]

print(">>> Printing Prices\n")

##################################################################
# OUTPUT
##################################################################
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.expand_frame_repr', False)
df = pd.DataFrame({'Artist': artist, 'Title': title, 'Best Price': best_price, 'Previous Price': previous_price, 'Current Price': current_price,'Price Change (%)': price_change})

# left align df
df.style.set_properties(**{'text-align': 'left'}).set_table_styles([ dict(selector='th', props=[('text-align', 'left')])])
df.to_csv('../output_data/records.csv', index=False, encoding='utf-8')

df = df[df['Current Price'] != 0]
terminal_output = df.sort_values(['Price Change (%)'], ascending=True).to_string(index=False)
print(terminal_output)

