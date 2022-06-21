import numpy as np #package for doing maths (linear algebra)
import pandas as pd #package for organising data into dataframes and organising it
import datetime as dt #access date and time
import requests #module for handling http requests
import matplotlib.pyplot as plt #plotting libraries (pyplot)
import cdflib #reading cdf's
import os #interface with OS
import seaborn as sns

class mageisInterface():

    #def __init__(self, data_view):


    def import_data(self):
        if os.stat('MagEISdata20160305.cdf').st_size == 0:
            print("Doing get request.")
            #THIS IS A LINK TO THE HOPE DATA NOT MAGEIS!!!!!!!!!!!!!
            url = f'https://spdf.gsfc.nasa.gov/pub/data/rbsp/rbspb/l2/ect/hope/spinaverage/rel04/2016/rbspb_rel04_ect-hope-sci-l2sa_20160305_v6.1.0.cdf'  # THIS NEEDS TOBE CHANGED
            r = requests.get(url)
            if r.status_code == 200:
                with open('MagEISdata20160305.cdf',
                          'wb') as file:  # CHANGE FILE IF URL THING GETS FIXED-ALREADY BEING USED BY HOPE
                    file.write(r.content)  # writng the content of the get request to file
                    self.mag_data = cdflib.CDF(
                        'MagEISdata20160305.cdf')  # using cdflib we read the data into CDF class object (makes it readable?)
        else:
            print("Reading from file.")
            with open('MagEISdata20160305.cdf', 'r') as file:
                self.mag_data = cdflib.CDF('MagEISdata20160305.cdf')

    def flux_time(self):
        #timeseries
        self.mag_times = [dt.datetime(1970,1,1) + dt.timedelta(seconds=i)
        for i in cdflib.epochs.CDFepoch.unixtime(self.mag_data.varget('Epoch'))]
        index = self.mag_times.index(dt.datetime(2016, 3, 5, 13, 15, 4, 614000))
        self.current_time = index

        #FESA series extraction for time t
        mag_fesa = np.array(self.mag_data.varget('FESA').T, dtype=float)
        log_mag_data = mag_fesa#np.log(mag_fesa)
        log_mag_data[log_mag_data == float('-inf')] == 0
        flux_selected_row = log_mag_data[0:72, index]

        #HOPE_ENERGY_Ele series extraction for time t
        mag_fedu = self.mag_data.varget('FEDU_Energy')
        electron_energy_array = mag_fedu

        return electron_energy_array, flux_selected_row

        #plot
        #fig, ax = plt.subplots()
        #ax.scatter(electron_energy_array / 1000, np.log(selected_row))  # e/1000 convert from eV -> KeV
        #ax.set_xlabel("HOPE_ENERGY_Ele [KeV]")
        #ax.set_ylabel("Log(Flux)")

