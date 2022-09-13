#Read in data A (energy and flux data, pandas dataframe)
#Read in data B (regression variables, pandas dataframe)
#Combine data via dates
#Apply pre-processing to data A
#Plot energy vs flux and regression lines (output as .png or .jpeg, named dynamically using f string (GOOGLE))
#Use ffmpeg library on the windows command line to concatonate images into a movie


import datetime as dt
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import gc

my_date = dt.date(2018, 1, 1)
df = pd.read_csv('2018-01-01.csv')

df.drop(df[df.Position < 2.7].index, inplace=True)
count = df["energy"].count()
print(count)

for i in range(3311, count):

    hope_energy = list(df.iloc[i]["hope_energy"].split(" "))
    hope_energy = list(map(float, filter(None, [s.strip("[").strip("]").strip("\n") for s in hope_energy])))

    mageis_energy = list(df.iloc[i]["mageis_energy"].split(" "))
    mageis_energy = list(map(float, filter(None, [s.strip("[").strip("]").strip("\n") for s in mageis_energy])))


    log_hope_psd = list(df.iloc[i]["log_hope_psd"].split(" "))
    log_hope_psd = list(map(float, filter(None, [s.strip("[").strip("]").strip("\n") for s in log_hope_psd])))

    log_mageis_psd = list(df.iloc[i]["log_mageis_psd"].split(" "))
    log_mageis_psd = list(map(float, filter(None, [s.strip("[").strip("]").strip("\n") for s in log_mageis_psd])))


    grad_1 = df.iloc[i]["Grad_1"]
    grad_2 = df.iloc[i]["Grad_2"]
    intercept_1 = df.iloc[i]["Intercept_1"]
    intercept_2 = df.iloc[i]["Intercept_2"]
    error = df.iloc[i]["Total_Error"]
    time = df.iloc[i]["HOPE_time"]
    position = df.iloc[i]["Position"]

    #time = df["HOPE_time"]
    #error = df["Total_Error"]
    #position = df["Position"]
    #plt.scatter(time, position)
    #plt.show()

    x_intercept = int((intercept_2 - intercept_1) / (grad_1 - grad_2))
    print(i)
    print(time)
    print(x_intercept)
    print(position)

    plt.close('all')

    fig, axes = plt.subplots(1, 1)
    axes.set_xlim(0, 4000)
    axes.set_ylim(20, 60)
    #axes.scatter(np.array(energy), np.array(log_psd))
    axes.scatter(np.array(hope_energy),np.array(log_hope_psd),)
    axes.scatter(np.array(mageis_energy), np.array(log_mageis_psd))
    axes.plot(list(range(0, x_intercept)), [((grad_1 * energy) + intercept_1) for energy in range(0, x_intercept)])
    axes.plot(list(range(0, 4000)), [((grad_2 * energy) + intercept_2) for energy in range(0, 4000)])
    axes.text(2500, 55, "time:")
    axes.text(2500, 53, time)
    axes.text(2500, 51, "position (L*):")
    axes.text(2500, 49, position)
    axes.text(2500, 47, "Total_Error:")
    axes.text(2500, 45, error)
    axes.set_xlabel("energy")
    axes.set_ylabel("log_psd")

    plt.savefig(f'data/images/{my_date}_{i}.jpeg')
    plt.close('all')
    gc.collect()



