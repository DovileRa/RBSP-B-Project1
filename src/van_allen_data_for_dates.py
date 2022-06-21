import datetime as dt
import os
from os.path import exists
import numpy as np
import cdflib
import pandas as pd
import psutil as psutil
import requests
import multiprocessing.dummy as mp
from src.linear_regression import linear_regression
from src.slicing_algorithm import slicing_algorithm
import traceback


#HOPE data importer
def hope_data_loader(date, url):
    year = date.year
    month = date.month

    if (month < 10):
        month = f'0{month}'
    day = date.day
    if (day < 10):
        day = f'0{day}'
    file_code = f"{year}{month}{day}"
    file_path = f'data/HOPE/{year}/{month}'
    file_name = f'/{file_code}.cdf'
    file_location = file_path + file_name
    if not (exists(file_location)):
        # if file size = 0, we need to get data and create a file to put it in
        print("Doing get request.")

        r = requests.get(url)  # using the request module, handle a http get request to the URL
        print(r.status_code)
        if r.status_code == 200:  # if request successful

            try:
                os.makedirs(file_path)
            except:
                print('path already exists')
            with open(file_location, 'wb') as file:  # open a file called HOPEdata20160305.cdf and name it file
                file.write(r.content)  # writng the content of the get request to file
                data = cdflib.CDF(file_location)  # using cdflib we read the data into CDF class object (makes it readable?)
        else:
            print('error code:', r.status_code, f'data {url} does not exist for {date}')
            data = []

    else:
        # reading the data from an already existing file in this directory
        print("Reading from file.")
        with open(file_location, 'r') as file:  # open the already existing file in 'read mode' and write it into cdf class
            data = cdflib.CDF(file_location)  # same as line 17


    return data

#MagEIS data importer
def mageis_data_loader(date, url):
    year = date.year
    month = date.month
    if (month < 10):
        month = f'0{month}'
    day = date.day
    if (day < 10):
        day = f'0{day}'
    file_code = f"{year}{month}{day}"
    file_path = f'data/MagEIS/{year}/{month}'
    file_name = f'/{file_code}.cdf'
    file_location = file_path + file_name
    if not (exists(file_location)):
        # if file size = 0, we need to get data and create a file to put it in
        print("Doing get request.")

        r = requests.get(url)  # using the request module, handle a http get request to the URL
        if r.status_code == 200:  # if request successful
            try:
                os.makedirs(file_path)
            except:
                print('path already exists')
            with open(file_location,'wb') as file:  # open a file called HOPEdata20160305.cdf and name it file
                file.write(r.content)  # writng the content of the get request to file
                data = cdflib.CDF(file_location)  # using cdflib we read the data into CDF class object (makes it readable?)
    else:
        # reading the data from an already existing file in this directory
        print("Reading from file.")
        with open(file_location, 'r') as file:  # open the already existing file in 'read mode' and write it into cdf class
            data = cdflib.CDF(file_location)  # same as line 17
    return data

#Taking natural logs and converting to keV
def data_pre_processing(hope_energy, hope_flux, mageis_energy, mageis_flux, position):

    hope_energy = hope_energy/1000 # eV -> keV

    # remove low count rates where HOPE > 25 keV
    low_count_index = np.where(hope_energy > 25)
    hope_energy = np.delete(hope_energy, low_count_index)
    hope_flux = np.delete(hope_flux, low_count_index)

    # remove low count rates where HOPE < 0.15 keV
    min_count_index = np.where(hope_energy < 0.15)
    hope_energy = np.delete(hope_energy, min_count_index)
    hope_flux = np.delete(hope_flux, min_count_index)

    neg_hope_flux_index = np.where(hope_flux <= 0)
    hope_flux = np.delete(hope_flux, neg_hope_flux_index)
    hope_energy = np.delete(hope_energy, neg_hope_flux_index)

    neg_mageis_flux_index = np.where(mageis_flux <= 0)
    mageis_flux = np.delete(mageis_flux, neg_mageis_flux_index)
    mageis_energy = np.delete(mageis_energy, neg_mageis_flux_index)

    neg_mageis_energy_index = np.where(mageis_energy <= 0)
    mageis_energy = np.delete(mageis_energy, neg_mageis_energy_index)
    mageis_flux = np.delete(mageis_flux, neg_mageis_energy_index)

    energy_series = np.append(hope_energy, mageis_energy)
    flux_series = np.append(hope_flux, mageis_flux)

    #neg_flux_index = np.where(flux_series <= 0)
    #neg_energy_index = np.where(energy_series <= 0)

    #flux_series = np.delete(flux_series, neg_flux_index)
    #energy_series = np.delete(energy_series, neg_flux_index)
    #flux_series = np.delete(flux_series, neg_energy_index)
    #energy_series = np.delete(energy_series, neg_energy_index)

    # calculating phase space density
    m = 9.1 * (10 ** -31)  # rest mass of an electron,kg
    c = 3 * (10 ** 8)  # speed of light, ms^-1

    hope_psd = hope_flux / (((hope_energy ** 2) + 2 * (m) * (c ** 2) * (hope_energy)) / (c ** 2))
    log_hope_psd = np.log(hope_psd)
    #log_hope_psd_neg_index = np.where(log_hope_psd < 0)
    #log_hope_psd = np.delete(log_hope_psd, log_hope_psd_neg_index)
    #hope_energy = np.delete(hope_energy, log_hope_psd_neg_index)

    mageis_psd = mageis_flux / (((mageis_energy ** 2) + 2 * (m) * (c ** 2) * (mageis_energy)) / (c ** 2))
    log_mageis_psd = np.log(mageis_psd)
    #log_mageis_psd_neg_index = np.where(log_mageis_psd < 0)
    #log_mageis_psd = np.delete(log_mageis_psd, log_mageis_psd_neg_index)
    #mageis_energy = np.delete(mageis_energy, log_mageis_psd_neg_index)



    phase_space_density = flux_series / (((energy_series ** 2) + 2 * (m) * (c ** 2) * (energy_series)) / (c ** 2))
    neg_index = np.where(phase_space_density < 0)

    phase_space_density = np.delete(phase_space_density, neg_index)
    energy_series = np.delete(energy_series, neg_index)
    #log_energy_series = np.log(energy_series)
    log_phase_space_density = np.log(phase_space_density)
    #print(log_energy_series,log_phase_space_density)
    #print(np.shape(log_energy_series), np.shape(log_phase_space_density))
    print('energy series shape',np.shape(energy_series))
    print('psd shape', np.shape(log_phase_space_density))

    return energy_series, log_phase_space_density, hope_energy, mageis_energy, log_hope_psd, log_mageis_psd

#Finds the nearest value in an array given a value
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def energy_flux_for_time(time,hope,mageis):
    #parameter times is an array where the first column is the HOPE times and the second is the MagEIS times
    #parameters HOPE and MagEIS are in CDF form

    #time is one row from the list of times
    hope_time = time[0] #first column
    mageis_time = time[1] #second column


    hope_times = [dt.datetime(1970, 1, 1) + dt.timedelta(seconds=i)
        for i in cdflib.epochs.CDFepoch.unixtime(hope.varget('Epoch_Ele'))]
    mag_times = [dt.datetime(1970, 1, 1) + dt.timedelta(seconds=i)
        for i in cdflib.epochs.CDFepoch.unixtime(mageis.varget('Epoch'))]

    hope_index = hope_times.index(hope_time)
    mag_index = mag_times.index(mageis_time)

    hope_energy = hope.varget('HOPE_ENERGY_Ele')[hope_index, 0:]
    mageis_energy = mageis.varget('FEDU_Energy')


    hope_flux = hope.varget('FESA')[hope_index,0:]
    mageis_flux = mageis.varget('FESA')[mag_index,0:]
    position = hope.varget('L_star_Ele')

    return hope_energy,hope_flux,mageis_energy,mageis_flux, position

def get_regression_variables(times, hope, mageis):
    #get energy and flux

    #time in times is one row where col 0 is hope and col 1 is mageis
    regression_variables = []
    multiple_regression_variables = []
    df = pd.DataFrame(
        columns=["HOPE_time", "MagEIS_time", "Grad", "Intercept", "Error", "Grad_1", "Intercept_1",
                 "Grad_2", "Intercept_2", "Total_Error","energy","log_psd","hope_energy", "mageis_energy", "log_hope_psd", "log_mageis_psd"])
    i = 0
    for time in times:

        hope_energy,hope_flux,mageis_energy,mageis_flux,position = energy_flux_for_time(time,hope,mageis)
        energy, log_psd, hope_energy_series, mageis_energy_series, log_hope_psd, log_mageis_psd = data_pre_processing(hope_energy,hope_flux,mageis_energy,mageis_flux,position)
        # single linear regression


        try:
            print(i)
            grad, intercept, error = linear_regression(energy, log_psd)
            grad_1, intercept_1, grad_2, intercept_2, error_2 = slicing_algorithm(energy, log_psd)
        except Exception as e:
            print(i,f'{e}',f'{traceback.format_exc()}')
            #print(i, "not enough data")
            grad_1, intercept_1, grad_2, intercept_2, error_2 = [0, 0, 0, 0,0]
        df.loc[i] = [*time, grad, intercept, error, grad_1, intercept_1, grad_2, intercept_2, error_2,energy,log_psd, hope_energy_series, mageis_energy_series, log_hope_psd, log_mageis_psd]

        i = i + 1

    return df

#Table construction
def join_hope_mageis(hope, mageis, date):
    pd.set_option('display.max_columns',1000)
    df = pd.DataFrame(columns=["HOPE_time", "MagEIS_time", "Position", "Grad", "Intercept", "Error", "Grad_1", "Intercept_1", "Grad_2", "Intercept_2", "Total_Error","energy","log_psd", "hope_energy", "mageis_energy", "log_hope_psd", "log_mageis_psd"])
    #pandas DataFrame containing series:
    print(hope.cdf_info()['zVariables'])
    print(mageis.cdf_info()['zVariables'])
    #Instrument name
    instrument_name = pd.Series()
    #Time
    hope_times = [dt.datetime(1970, 1, 1) + dt.timedelta(seconds=i)
                       for i in cdflib.epochs.CDFepoch.unixtime(hope.varget('Epoch_Ele'))]
    mageis_times = [dt.datetime(1970, 1, 1) + dt.timedelta(seconds=i)
                       for i in cdflib.epochs.CDFepoch.unixtime(mageis.varget('Epoch'))]

    times = []
    i = 0

    #for time in hope_times:
    ####WHY DO I START AT THIS INDEX?
    for time in hope_times[0:]:
        i = i+1
        times.append([time, find_nearest(mageis_times, time)])
        if i % 50 == 0:
            print(i, time)
    print('hope times', np.size(hope_times))
    times = np.array(times)
    position = hope.varget('L_star_Ele')

    df["Position"] = position
    df["MagEIS_time"] = times[:, 1]
    df["HOPE_time"] = times[:, 0]



    # extract flux and energy fora time 2018-01-01 00:00:00.941 2018-01-01 00:00:07.503

    #get regression variables
    regression_variables = get_regression_variables(times, hope, mageis) #[g,i,e], [g,i,g2,i2,e]

    df.update(regression_variables)

    #print(regression_variables)
    #print("TABLE:")
    print(df)
    df.to_csv(f'{date}.csv', index = True)
    return

def test(hope, mageis):
    hope_energy = hope.varget('HOPE_ENERGY_Ele')[0, 0:]
    mageis_energy = mageis.varget('FEDU_Energy')
    #print(mageis_energy)
    #print(mageis.cdf_info())


class Van_allen_data_loader():

    def __init__(self, date, date_string, hope_url, mageis_url):
        #init is automatically called by python when the class is instantiated
        self.date_string = date_string
        self.date = date #set class variable date = to input date
        self.hope_url = hope_url
        self.mageis_url = mageis_url
        self.hope_data = hope_data_loader(date, hope_url) #hopedata is a cdf file
        self.mageis_data = mageis_data_loader(date, mageis_url) #so is mageis
        #self.test = test(self.hope_data, self.mageis_data)
        self.data_table = join_hope_mageis(self.hope_data, self.mageis_data, self.date_string)

my_date = dt.date(2018, 1, 1)

#print(psutil.cpu_count())
#data = Van_allen_data_loader(my_date)

#print(data.date)
#print(data.hope_data)
#print(data.mageis_data)
