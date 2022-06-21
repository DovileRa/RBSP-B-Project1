import datetime as dt
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import gc

my_date = dt.date(2018, 1, 1)

df = pd.read_csv('2018-01-01.csv')

count = df["energy"].count()
print(count)

for i in range(0,count):
    print(i)

    df.drop(df[df.Position < 2.7].index, inplace=True)
    #df.drop(df[df.Error < 50].index, inplace=True)
    print('size:',np.shape(df["energy"]))
    energy = list(df.iloc[i]["energy"].split(" "))
    #print(energy)
    energy = list(map(float, filter(None, [s.strip("[").strip("]").strip("\n") for s in energy])))

    log_psd = list(df.iloc[i]["log_psd"].split(" "))
    log_psd = list(map(float, filter(None, [s.strip("[").strip("]").strip("\n") for s in log_psd])))
    grad_1 = df.iloc[i]["Grad_1"]
    grad_2 = df.iloc[i]["Grad_2"]
    intercept_1 = df.iloc[i]["Intercept_1"]
    intercept_2 = df.iloc[i]["Intercept_2"]
    error = df.iloc[i]["Total_Error"]
    time = df.iloc[i]["HOPE_time"]
    position = df.iloc[i]["Position"]

    error = df["Error"]
    position = df["Position"]
    # print('error',error)
    print('position', position)
    plt.scatter(position, error)
    #plt.show()

    x_intercept = int((intercept_2 - intercept_1) / (grad_1 - grad_2))
    print(i)
    print(time)
    print(x_intercept)

    plt.close('all')

    fig, axes = plt.subplots(1, 1)
    axes.scatter(np.array(energy), np.array(log_psd))
    axes.plot(list(range(0, x_intercept)), [((grad_1 * energy) + intercept_1) for energy in range(0, x_intercept)])
    axes.plot(list(range(0, 4000)), [((grad_2 * energy) + intercept_2) for energy in range(0, 4000)])
    #axes.text(2500, 55, "time:")
    #axes.text(2500, 53, time)
    #axes.text(2500, 51, "position (L*):")
    #axes.text(2500, 49, position)
    #axes.text(2500, 47, "error:")
    #axes.text(2500, 45, error)
    axes.set_xlabel("energy")
    axes.set_ylabel("log_psd")

    plt.savefig(f'data/error_images/{my_date}_{i}.jpeg')
    plt.close('all')
    gc.collect()



