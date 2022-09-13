

import datetime
import os
from os.path import exists
import cdflib
import requests
import van_allen_data_for_dates as van_allen
import pandas as pd
from datetime import datetime

def main():
    #list of urls
    df = pd.read_csv('date_list.csv')
    hope_url_list = df['hope_url']
    mageis_url_list = df['mageis_url']
    date_list = df['date']

    i = 0

    #iterate through that list
    for hope_url in hope_url_list:
        #may need to convert url to date
        print(date_list[i])
        van_allen.Van_allen_data_loader(datetime.strptime(date_list[i], '%Y-%m-%d'),date_list[i], hope_url, mageis_url_list[i])

        i = i+1
    #for each iteration, apply van allen algorithm


    return


main()
