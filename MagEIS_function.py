import numpy as np  #package for doing maths (linear algebra)
import pandas as pd  #package for organising data into dataframes and organising it
import datetime as dt  #access date and time
import requests  #module for handling http requests
import matplotlib.pyplot as plt  #plotting libraries (pyplot)
import cdflib  #reading cdf's
import os  #interface with OS
import csv
import pandas
import seaborn as sns

#######################################################################################################################
# READING IN MagEIS DATA
if os.stat('MagEISdata20160305.cdf').st_size == 0:
    print("Doing get request.")
    url = 'https://spdf.gsfc.nasa.gov/pub/data/rbsp/rbspb/l2/ect/hope/spinaverage/rel04/2016/rbspb_rel04_ect-hope-sci-l2sa_20160305_v6.1.0.cdf' #THIS NEEDS TOBE CHANGED
    r = requests.get(url)
    if r.status_code == 200:
        with open('MagEISdata20160305.cdf', 'wb') as file:  #CHANGE FILE IF URL THING GETS FIXED-ALREADY BEING USED BY HOPE
            file.write(r.content)  #writng the content of the get request to file
            data = cdflib.CDF('MagEISdata20160305.cdf')  #using cdflib we read the data into CDF class object (makes it readable?)
else:
    print("Reading from file.")
    with open('MagEISdata20160305.cdf', 'r') as file:
        MagEISdata = cdflib.CDF('MagEISdata20160305.cdf')

########################################################################################################################
#INFORMATION ABOUT MagEIS VARIABLES
#print("here",MagEISdata.attinq())
print(MagEISdata.cdf_info()['zVariables'])
print(MagEISdata.varattsget('FESA'))
#MagEIS_electron_energy_atts = data.varattsget('HOPE_ENERGY_Ele')
#print(electron_energy_atts)
#print(MagEISdata.varget('FESA_Energy'))

MagEISdataframe = pandas.DataFrame(MagEISdata.varget('FESA'))
print("overhere")
print(MagEISdataframe)

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
# PLOT FOR A ENERGY/FLUX FOR A SPECIFIC TIME FOR MagEIS

#Converting to datetime
MagEIS_times = [dt.datetime(1970,1,1) + dt.timedelta(seconds=i)
 for i in cdflib.epochs.CDFepoch.unixtime(MagEISdata.varget('Epoch'))]

MagEIS_electron_energy = MagEISdata.varget('FEDU_Energy')
print(MagEIS_electron_energy)
print("shape:", np.shape(MagEIS_times))
for item in MagEISdata.cdf_info()['zVariables']:
    try:
        #print(f'shape {item}:', np.shape(MagEISdata.varget(f'{item}')))
        continue
    except:
        continue






#Finding the index of the time specified
print('index',MagEIS_times.index(dt.datetime(2016, 3, 5, 13, 15, 4, 614000)))
MagEIS_index = MagEIS_times.index(dt.datetime(2016, 3, 5, 13, 15, 4, 614000))

index = MagEIS_times.index(dt.datetime(2016, 3, 5, 13, 15, 4, 614000))
print(log_MagEISdata)

selected_row = log_MagEISdata[0:72, index]
print(MagEIS_electron_energy)

MagEIS_electron_energy_array = MagEIS_electron_energy
fig,ax = plt.subplots()
fig2,ax2 = plt.subplots()

print(MagEIS_electron_energy_array,selected_row)
ax.scatter(MagEIS_electron_energy_array/1000, np.log(selected_row)) #e/1000 convert from eV -> KeV
ax.set_xlabel("MagEIS_ENERGY_Ele [KeV]")
ax.set_ylabel("Log(Flux)")

fig, ax = plt.subplots(1,1)
fig.show();
fig2.show();
plt.show();

#print('index = ', times.index((2016, 3, 5, 13, 15, 40)))



