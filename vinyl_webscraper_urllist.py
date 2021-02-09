from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from bs4 import BeautifulSoup
import pandas as pd

##################################################################
# INTIALISING DATA STORAGE
##################################################################

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path='/Users/jcmunday/Documents/Computing/webscraper/chromedriver', options=chrome_options)
url_list = open("urls.txt", "r")
content = url_list.read()
urls = content.splitlines()

size = len(urls)
title = [0 for _ in range(size)]
artist = [0 for _ in range(size)]
current_price = [0 for _ in range(size)]
price_change = [0 for _ in range(size)]

try:
    records_df = pd.read_csv('records.csv')
    best_price = records_df['Best Price'].tolist()
except:
    best_price = [0 for _ in range(size)]
print(">>> Fetching Record Prices")
##################################################################
# SCRAPPING DATA
##################################################################
for indx, url in enumerate(urls):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    artist_tmp = soup.find('span', attrs={'class': 'author notFaded'}).get_text()
    artist_tmp  = artist_tmp.split('\n')
    if type(artist_tmp[1])==str:
        artist[indx] = artist_tmp[1]

    name = soup.find('title').get_text()
    if "[VINYL]" in name:
        name, _ = name.split(' [VINYL]')
    if artist[indx] in name:
        name = name.strip(artist[indx])
        if not name:
            name = "Self Titled"
    title[indx] = name

    price = soup.find('span', id="price_inside_buybox")
    if price is None:
        pass
    else:
        price = price.get_text()
        price = price.strip('\n')
        price = float(price.strip('£'))
    current_price[indx] = price

    if price is not None:
        if best_price[indx]==0:
            best_price[indx] = price
            price_change[indx] = 0
        elif best_price[indx] > price:
            price_change[indx] = price - best_price[indx]
            best_price[indx] = price
        else:
            price_change[indx] = current_price[indx] - best_price[indx]
price_change = [round(elem, 2) for elem in price_change]
driver.quit()
print(">>> Priting Prices")

##################################################################
# OUTPUT
##################################################################
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.expand_frame_repr', False)
df = pd.DataFrame({'Artist': artist, 'Title': title, 'Current Price': current_price, 'Best Price': best_price, 'Price Change': price_change})
df.to_csv('records.csv', index=False, encoding='utf-8')

terminal_output = df.sort_values(['Price Change'], ascending=True)
print(terminal_output)

