import numpy as np #package for doing maths (linear algebra)
import pandas as pd #package for organising data into dataframes and organising it
import datetime as dt #access date and time
import requests #module for handling http requests
import matplotlib.pyplot as plt #plotting libraries (pyplot)
import cdflib #reading cdf's
import os #interface with OS
import seaborn as sns
########################################################################################################################
#T HIS BLOCK READS IN THE HOPE DATA

if os.stat('HOPEdata20160305.cdf').st_size == 0:  #using OS, we are looking for HOPEdata20160305.cdf in the directory that we are in, checking its size, if the size is 0 then it does not exist
    #if file size = 0, we need to get data and create a file to put it in
    print("Doing get request.")
    url = 'https://spdf.gsfc.nasa.gov/pub/data/rbsp/rbspb/l2/ect/hope/spinaverage/rel04/2016/rbspb_rel04_ect-hope-sci-l2sa_20160305_v6.1.0.cdf' # setting up target URL
    r = requests.get(url) #using the request module, handle a http get request to the URL
    if r.status_code == 200: #if request successful
        with open('HOPEdata20160305.cdf', 'wb') as file: #open a file called HOPEdata20160305.cdf and name it file
            file.write(r.content) #writng the content of the get request to file
            data = cdflib.CDF('HOPEdata20160305.cdf') #using cdflib we read the data into CDF class object (makes it readable?)
else:
    #reading the data from an already existing file in this directory
    print("Reading from file.")
    with open('HOPEdata20160305.cdf', 'r') as file: #open the already existing file in 'read mode' and write it into cdf class
        HOPEdata = cdflib.CDF('HOPEdata20160305.cdf') #same as line 17

########################################################################################################################
#INFORMATION ABOUT HOPE VARIABLES

#print(data.cdf_info()['zVariables'])
#print(data.varattsget('FESA'))
#electron_energy_atts = data.varattsget('HOPE_ENERGY_Ele')
#print(electron_energy_atts)

########################################################################################################################
# THIS BLOCK CREATES A PLOT OF ENERGY/FLUX FOR ALL TIMES FOR HOPE

HOPE_FESA = np.array(HOPEdata.varget('FESA').T,dtype=float)

log_HOPEdata = np.log10(HOPE_FESA)
log_HOPEdata[log_HOPEdata==float('-inf')] == 0

plt.imshow(log_HOPEdata,aspect='auto',origin='lower',cmap='plasma')#plotting log of the data

plt.colorbar()

plt.show();

########################################################################################################################
# THIS BLOCK CREATES A PLOT FOR ENERGY/FLUX FOR A SPECIFIC TIME FOR HOPE

#Converting to datetime
HOPE_times = [dt.datetime(1970,1,1) + dt.timedelta(seconds=i)
 for i in cdflib.epochs.CDFepoch.unixtime(HOPEdata.varget('Epoch_Ele'))]



HOPE_electron_energy = HOPEdata.varget('HOPE_ENERGY_Ele')



#Finding the index of the time specified
#print('index',times.index(dt.datetime(2016, 3, 5, 13, 15, 17, 303000)))
index = HOPE_times.index(dt.datetime(2016, 3, 5, 13, 15, 17, 303000))

selected_row = log_HOPEdata[0:72, index]
electron_energy_array = HOPE_electron_energy[index, 0:72]
fig,ax = plt.subplots()
fig2,ax2 = plt.subplots()

#print(electron_energy_array,selected_row)
ax.scatter(electron_energy_array/1000, np.log(selected_row)) #e/1000 convert from eV -> KeV
ax.set_xlabel("HOPE_ENERGY_Ele [KeV]")
ax.set_ylabel("Log(Flux)")

#fig, ax = plt.subplots(1,1)

#print('index = ', times.index((2016, 3, 5, 13, 15, 40)))

#######################################################################################################################
# READING IN MagEIS DATA
if os.stat('MagEISdata20160305.cdf').st_size == 0:
    print("Doing get request.")
    url = 'https://spdf.gsfc.nasa.gov/pub/data/rbsp/rbspb/l2/ect/hope/spinaverage/rel04/2016/rbspb_rel04_ect-hope-sci-l2sa_20160305_v6.1.0.cdf' #THIS NEEDS TOBE CHANGED
    r = requests.get(url)
    if r.status_code == 200:
        with open('MagEISdata20160305.cdf', 'wb') as file: #CHANGE FILE IF URL THING GETS FIXED-ALREADY BEING USED BY HOPE
            file.write(r.content) #writng the content of the get request to file
            data = cdflib.CDF('MagEISdata20160305.cdf') #using cdflib we read the data into CDF class object (makes it readable?)
else:
    print("Reading from file.")
    with open('MagEISdata20160305.cdf', 'r') as file:
        MagEISdata = cdflib.CDF('MagEISdata20160305.cdf')

########################################################################################################################
# INFORMATION ABOUT MagEIS VARIABLES

print(MagEISdata.cdf_info()['zVariables'])
#print(MagEISdata.varattsget('FESA'))
#electron_energy_atts = data.varattsget('HOPE_ENERGY_Ele')
#print(electron_energy_atts)

########################################################################################################################
# THIS BLOCK CREATES A PLOT OF ENERGY/FLUX FOR ALL TIMES FOR MagEIS

MagEIS_FESA = np.array(MagEISdata.varget('FESA').T,dtype=float)

log_MagEISdata = np.log10(MagEIS_FESA)
log_MagEISdata[log_MagEISdata==float('-inf')] == 0
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
im2 = ax2.imshow(log_MagEISdata,aspect='auto',origin='lower',cmap='plasma')#plotting log of the data

fig2.colorbar(im2)
########################################################################################################################


########################################################################################################################
fig.show();
fig2.show();
plt.show();
