from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#import chromedriver_binary
from bs4 import BeautifulSoup
import pandas as pd

##################################################################
# INTIALISING DATA STORAGE
##################################################################
#chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox")
#driver = webdriver.Chrome(executable_path='/Users/jcmunday/Documents/Computing/webscraper/chromedriver', options=chrome_options)

driver = webdriver.Safari()
url_list = open("urls.txt", "r")
content = url_list.read()
urls = content.splitlines()

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
    #assert len(best_price) == len(title), "Mismatched number of records in url.txt to that stored in records.csv"
except:
    best_price = [0 for _ in range(size)]
    previous_price = [0 for _ in range(size)]

print("\n>>> Fetching Record Prices")
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
    
    if price is not None:
        price = price.get_text()
        price = price.strip('\n')
        price = float(price.strip('£'))
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
df.to_csv('records.csv', index=False, encoding='utf-8')

df = df[df['Current Price'] != 0]
terminal_output = df.sort_values(['Price Change (%)'], ascending=True).to_string(index=False)
print(terminal_output)

