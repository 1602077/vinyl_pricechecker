#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# webscraper.py
# Author: Jack Munday
#
# Web scraper implementation using selenium and BeautifulSoup to automate the price checking of records in my amazon wishlist. Input file "urls.txt" should be a list of amazon urls with one url per line. Script then cycles through all urls and get the current artist name, record title and price. This is outputted to "records_history.csv" which contains a unique column of prices for all records in the wish list every time the script is ran. Summary statistics of all the historic data are then outputted to "records_summary.csv" containing the best price, current and average prices.


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import pdb


pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.expand_frame_repr', False)


def records_wishlist_scraper(driver, url, price_only=False):
    """
    Web scraper to scrape the artist name, record title and current price for a given record as listed on amazon
    specified by the url.

    params:
    ------------------------------------------------------------------------------------------------------------
    driver:         Selenium instance of the driver for the browser being used to perform the web scraping
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

    # comment below if you decide to run in chrome
    driver = webdriver.Safari()

    # To use chrome instead import the above libraries and download the chromedriver file for your os
    # below provides some options that you may want to consider using, headless is a particularly useful
    # one as it runs the browsers without a gui.
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox")
    #driver = webdriver.Chrome(executable_path='/filepath_to_chromedriver/chromedriver', options=chrome_options)

    # import list of amazon urls for records in wishlist and convert to a python list
    #url_list = open("../input_data/urls.txt", "r")
    input_file = open("../input_data/urls_test.txt", "r")
    input_urls = input_file.read().splitlines()

    # Get current datetime
    today = pd.to_datetime("today")

    ##################################################################
    # CREATE PANDAS DATAFRAME
    ##################################################################
    try: 
        records_df = pd.read_csv('../output_data/records_history.csv')
    except:
        # if there is no records df already initiate an empty pd df
        # only executes on the first run of the code, subsequent runs will add price columns to
        # keep track of history of price changes
        # date time column will hold the price of a given record for current date
        column_names = ['url', 'Artist Name', 'Record Title', str(today)]
        records_df = pd.DataFrame(columns=column_names)

    ##################################################################
    # SCRAPPING DATA (HISTORICAL PRICING)
    ##################################################################
    # find any new records that have been added to urls.txt
    existing_records = records_df['url'].tolist()
    new_records = [url for url in input_urls if url not in existing_records]

    print(f"{len(new_records)} new record(s) in wishlist!")

    # get the current price of existing records in the dataframe and add as a new col
    records_df[str(today)] = records_df['url'].apply(lambda url:records_wishlist_scraper(driver, url, price_only=True))

    # add new records into the historic price dataframe and append as a new row
    for url in new_records:
        artist_name, record_name, price = records_wishlist_scraper(driver, url)
        df_tmp = pd.DataFrame({'url': url, 'Artist Name': artist_name, 'Record Title': record_name, str(today): price}, index=[0])
        records_df = records_df.append(df_tmp, ignore_index=True)

    driver.quit()

    records_df.to_csv('../output_data/records_history.csv', index=False, encoding='utf-8')

    ##################################################################
    # SUMMARISING HISTORICAL DATA
    ##################################################################
    summary_df = pd.DataFrame({
                'Artist Name':      records_df['Artist Name'],
                'Record Title':     records_df['Record Title'],
                'Best Price':       records_df.min(axis=1, numeric_only=True),
                'Average Price':    records_df.mean(axis=1, numeric_only=True).round(2),
                'Current Price':    records_df[records_df.columns[-1]]
     })

    num_records = summary_df.shape[0]
    best_price = summary_df['Best Price'].sum()
    current_price = summary_df['Current Price'].sum()

    #Calculating some high level stats about wishlist records
    print()
    print(f"Number of records in wishlist: {num_records}.")
    print(f"Best cost to buy all records in wishlist: {best_price}.")
    print(f"Current cost to buy all records in wishlist: {current_price}.")
    print()
     
    summary_df.style.set_properties(**{'text-align': 'left'}).set_table_styles([ dict(selector='th', props=[('text-align', 'left')])])
    summary_df = summary_df.sort_values(['Artist Name'], ascending=True).reset_index(drop=True)
    print(summary_df)

    return summary_df.to_csv('../output_data/records_summary .csv', index=False, encoding='utf-8')

    
if __name__ == "__main__":
    main()

