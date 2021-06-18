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
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

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


def plot_records(record_titles):
    """
    Helper function to automate plotting historical pricing data of records

    params:
    --------------------------------------------------------------------------
    record_titles:   list of record titles to be plotted

    returns:
    --------------------------------------------------------------------------
    plot of the historical pricing data for specified records in record_title
    """

    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.expand_frame_repr", False)
    history_data = pd.read_csv('../output_data/records_history.csv',  encoding='utf-8')
    drop_cols = ['url', 'Artist Name']

    history_data.drop(columns=drop_cols, inplace=True)
    history_data = history_data.melt(id_vars = ['Record Title'], var_name = 'Date', value_name = 'Price')
    history_data['Date'] = pd.to_datetime(history_data['Date']).dt.date
    history_data = history_data[history_data['Record Title'].isin(record_titles)]

    mpl.rcParams['font.family']='serif'
    cmfont = fm.FontProperties(fname=mpl.get_data_path() + '/fonts/ttf/cmr10.ttf')
    mpl.rcParams['font.serif']=cmfont.get_name()
    mpl.rcParams['mathtext.fontset']='cm'
    mpl.rcParams['text.usetex'] = True
    #mpl.rcParams['axes.unicode_minus']=False


    fig = plt.figure(figsize=(14,8))
    ax = plt.subplot(111)
    sns.lineplot(data=history_data, x='Date', y='Price', hue='Record Title')
    
    ax.tick_params(direction='in', length=6, width=1, colors='k', top=True, right=True)
    ax.set_xlabel("Date", labelpad=15, fontsize=16, color="#333533");
    ax.set_ylabel("Price (\pounds)", labelpad=16, fontsize=14, color="#333533")
    lgd = ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), ncol=2, fancybox=True, shadow=True, title='Albums', fontsize=14, title_fontsize=15)
    #plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.setp(ax.get_xticklabels(), fontsize=14)
    plt.setp(ax.get_yticklabels(), fontsize=14)

    plt.title('Historical Pricing Data of Records', fontsize=15, color="#333533")
    plt.tight_layout()
    plt.savefig('../plots/historical_data.png', dpi=500, transparent=False, bbox_inches='tight')#, bbox_extra_artists=(lgd,))

    return


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
    #main()
    plot_records(["Continuum", "Beat Tape 1", "Holy Fire", "Songs In The Key Of Life", "What Went Down", "Venice (180g Vinyl)"])
