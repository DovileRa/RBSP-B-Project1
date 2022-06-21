import numpy as np #package for doing maths (linear algebra)
import pandas as pd #package for organising data into dataframes and organising it
import datetime as dt #access date and time
import requests #module for handling http requests
import matplotlib.pyplot as plt #plotting libraries (pyplot)
import cdflib #reading cdf's
import os #interface with OS
import seaborn as sns

class hopeInterface():

    #def __init__(self, data_view):


    def import_data(self):
        if os.stat(
                'HOPEdata20160305.cdf').st_size == 0:  # using OS, we are looking for HOPEdata20160305.cdf in the directory that we are in, checking its size, if the size is 0 then it does not exist
            # if file size = 0, we need to get data and create a file to put it in
            print("Doing get request.")
            url = 'https://spdf.gsfc.nasa.gov/pub/data/rbsp/rbspb/l2/ect/hope/spinaverage/rel04/2016/rbspb_rel04_ect-hope-sci-l2sa_20160305_v6.1.0.cdf'  # setting up target URL
            r = requests.get(url)  # using the request module, handle a http get request to the URL
            if r.status_code == 200:  # if request successful
                with open('HOPEdata20160305.cdf',
                          'wb') as file:  # open a file called HOPEdata20160305.cdf and name it file
                    file.write(r.content)  # writng the content of the get request to file
                    self.hope_data = cdflib.CDF(
                        'HOPEdata20160305.cdf')  # using cdflib we read the data into CDF class object (makes it readable?)
        else:
            # reading the data from an already existing file in this directory
            print("Reading from file.")
            with open('HOPEdata20160305.cdf',
                      'r') as file:  # open the already existing file in 'read mode' and write it into cdf class
                self.hope_data = cdflib.CDF('HOPEdata20160305.cdf')  # same as line 17

    def flux_time(self):
        #timeseries
        self.hope_times = [dt.datetime(1970,1,1) + dt.timedelta(seconds=i)
        for i in cdflib.epochs.CDFepoch.unixtime(self.hope_data.varget('Epoch_Ele'))]
        index = self.hope_times.index(dt.datetime(2016, 3, 5, 13, 15, 17, 303000))

        #FESA series extraction for time t
        HOPE_FESA = np.array(self.hope_data.varget('FESA').T, dtype=float)
        log_HOPEdata = HOPE_FESA#np.log(HOPE_FESA)
        log_HOPEdata[log_HOPEdata == float('-inf')] == 0
        flux_selected_row = log_HOPEdata[0:72, index]

        #HOPE_ENERGY_Ele series extraction for time t
        HOPE_electron_energy = self.hope_data.varget('HOPE_ENERGY_Ele')
        electron_energy_array = HOPE_electron_energy[index, 0:72]
        return electron_energy_array,flux_selected_row

        #plot
        #fig, ax = plt.subplots()
        #ax.scatter(electron_energy_array / 1000, np.log(selected_row))  # e/1000 convert from eV -> KeV
        #ax.set_xlabel("HOPE_ENERGY_Ele [KeV]")
        #ax.set_ylabel("Log(Flux)")

