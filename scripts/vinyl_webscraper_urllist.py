# vinyl_webscraper_urllist.py
#
# Author: Jack Munday
#
# Webscraper implimentation using selenium and BeautifulSoup to automate the price checking of records in my amazon wishlist. Input file "urls.txt" should be a list of amazon urls with one url per line. Script then cyclesthrough all urls and get the current artist name, record title and price. Through comparing this price to the  current output data file "recpods.csv" it keeps track of the best price and calculates any % price changes.


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import pdb


pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.expand_frame_repr', False)


def records_wishlist_scraper(driver, url, price_only=False):
    """
    Webscraper to scrape the Artist Name, Record Title and Current Price for a given record as listed on Amazon
    specified by the url.

    params:
    ------------------------------------------------------------------------------------------------------------
    driver:         Selenium instance of the driver for the browser being used to perform the webscraping
                    e.g. driver = webdriver.Safari()
    url:            Amazon url for a given record whose price you would like to keep track of
    price_only:     Boolean, if True scraper only returns the price for the record as specified in url. This is
                    useful for records already with historic price data as we already know the artist name,
                    and record title associated with that given url.
    returns:
    ------------------------------------------------------------------------------------------------------------
    artist_name:    Name of artist for the record specified by the input url
    record_name:    Title of record for the input url
    price:          Current price of record_title
    """

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    artist = soup.find('span', attrs={'class': 'author notFaded'}).get_text()
    artist_name  = str(artist.split('\n')[1])

    record_name = soup.find('title').get_text()
    # strip [VINYL] suffixes that amazon adds to records
    if "[VINYL]" in record_name:
        record_name, _ = record_name.split(' [VINYL]')

    # Remove artist name from title for improperly listed records
    if artist_name in record_name:
        record_name = record_name.strip(artist_name)
        if not record_name:
            record_name = "Self Titled"

    price = soup.find('span', id="price_inside_buybox")
    
    if price is not None:
        price = price.get_text()
        price = price.strip('\n')
        price = float(price.strip('£'))

    return [artist_name, record_name, price] if price_only==False else price

##################################################################
# USING CHROME INSTEAD OF SAFARI
##################################################################
#from selenium.webdriver.chrome.options import Options
#import chromedriver_binary


def main():
    """

    """

    # To use chrome instead import the above libraries and download the chromedriver file for your os
    # below provides some options that you may want to consider using, headless is a particularly useful
    # one as it runs the browers without a gui.
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox")

    #driver = webdriver.Chrome(executable_path='/filepath_to_chromedriver/chromedriver', options=chrome_options)

    # comment below if you decide to run in chrome
    driver = webdriver.Safari()

    # import list of amazon urls for records in wishlist and convert to a python list
    #url_list = open("../input_data/urls.txt", "r")
    url_list = open("../input_data/urls_test.txt", "r")
    #content = url_list.read()
    input_urls = url_list.read().splitlines()

    # Get current datetime
    today = pd.to_datetime("today")

    ##################################################################
    # CREATE PANDAS DATAFRAME
    ##################################################################
    try: 
        records_df = pd.read_csv('../output_data/records_history.csv')
    except:
        # if there is no records df already initiate an empty pd df
        # only executes on the first run of the code, subseqeunt runs will add price columns to
        # keep track of history of price changes
        # datetime column will hold the price of a given record for current date
        column_names = ['url', 'Artist Name', 'Record Title', str(today)]
        records_df = pd.DataFrame(columns=column_names)

    ##################################################################
    # SCRAPPING DATA (HISTORICAL PRICING)
    ##################################################################

    # find any new records that have been added to urls.txt
    existing_records = records_df['url'].tolist()
    new_records = [url for url in input_urls if url not in existing_records]

    print(f"{len(new_records)} new record(s) in wishlist!")
    #print("\n>>> Fetching Record Prices")

    # get the current price of existing records in the dataframe and add as a new col
    records_df[str(today)] = records_df['url'].apply(lambda url:records_wishlist_scraper(driver, url, price_only=True))

    # add new records into the historic price dataframe as new rows
    for url in new_records:
        artist_name, record_name, price = records_wishlist_scraper(driver, url)
        df_tmp = pd.DataFrame({'url': url, 'Artist Name': artist_name, 'Record Title': record_name, str(today): price}, index=[0])
        records_df = records_df.append(df_tmp, ignore_index=True)

    driver.quit()

    records_df.to_csv('../output_data/records_history.csv', index=False, encoding='utf-8')

    ##################################################################
    # OUTPUT
    ##################################################################
    #print(">>> Printing Prices\n")

    #df.style.set_properties(**{'text-align': 'left'}).set_table_styles([ dict(selector='th', props=[('text-align', 'left')])])

    #df = df[df['Current Price'] != 0]
    #terminal_output = df.sort_values(['Artist'], ascending=True).to_string(index=False)
    #print(terminal_output)

    #Calculating some high level stats about wishlist records
    #num_records = len(input_urls)
    # best_price = record_df[''].sum()
    #current_price = records_df[str(today)].sum()
    #print(f"Number of records in wishlist: {num_records}.")
    #print(f"Best cost to buy all records in wishlist: {best_price}.")
    #print(f"Current cost to buy all records in wishlist: {current_price}.")

if __name__ == "__main__":
    main()

