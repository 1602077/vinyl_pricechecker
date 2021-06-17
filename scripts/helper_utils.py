#!/Users/jcmunday/miniforge3/envs/web_s/bin/python
# -*- coding: utf-8 -*-
#
# helper_utils.py
# author: Jack Munday
#
# Series of helper functions to compliment webscraper.py: making it easier to add / remove records
# and plot their historical price.


import os
import pandas as pd


def remove_record(record_title):
    """
    Helper function to automate removing a record from wish list (urls.txt)
    and remove all pricing data (*.csv in ../output_data/).

    params:
    --------------------------------------------------------------------------
    record_title:   title of the record to be removed from wish list

    returns:
    ---------------------------------------------------------------------------
    Rows corresponding to record_title will be removed from the files below:
    urls.txt
    records_history.csv
    records_summary.csv
    """

    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.expand_frame_repr", False)
    
    # remove record from pricing dataframe
    for name in ['history', 'summary']: 
        df = pd.read_csv('../output_data/records_' + str(name) + '.csv')

        # get index position of record_title in dataframe
        try:
            indx = df[df['Record Title'] == record_title].index[0]
        except:
            print("Input Record not found in data.")
            return 0
        if name == 'history':
            url = df.loc[indx, 'url']

        # remove this record from df
        df.drop(df.index[indx], inplace=True)
        df.to_csv('../output_data/records_' + str(name) + '.csv', index=False)

    # using the url picked up in the history iteration, rm url from input file
    with open('../input_data/urls.txt', "r") as f:
        lines = f.readlines()
        
    with open('../input_data/urls.txt', "w") as f:
        for line in lines:
            if line.strip("\n") != url:
                f.write(line)

    return 1


def main():

    function_type = input("Would you like to add, remove or plot records (A/R/P)?\n")

    if function_type.lower() == "r" or function_type.lower() == "remove":
        record_to_rm = input("Please type a record title to remove from record list\n")
        removed_records = remove_record(record_to_rm)
        
        if removed_records == 1:
            print(str(record_to_rm) + ' removed from wishlist and historical data cleared.')

    if function_type.lower() == "p" or function_type.lower() == "plot":
        pass

    if function_type.lower() == "a" or function_type.lower() == "add":
        pass

    if function_type.lower() == "q" or function_type.lower() == "quit":
       return  1

    user_action = input('Press "r" to re-run again or any other key to escape.\n')

    return main() if user_action == "r" else 0


if __name__ == "__main__":
    #remove_record("Test Album")
    main()
