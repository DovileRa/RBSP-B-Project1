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

for i in range(0, count):
    energy = list(df.iloc[i]["energy"].split(" "))
    energy = list(map(float, filter(None, [s.strip("[").strip("]").strip("\n") for s in energy])))

    log_psd = list(df.iloc[i]["log_psd"].split(" "))
    log_psd = list(map(float, filter(None, [s.strip("[").strip("]").strip("\n") for s in log_psd])))

    parameters = np.polyfit(energy,log_psd,2)
    poly = np.poly1d(parameters)
    print(poly)

    new_x = []
    new_y = []
    for j in range(count):
        new_x.append(j+1)
        calc = poly(j+1)
        new_y.append(calc)

    plt.xlim(0, 4000)
    plt.ylim(20, 60)
    plt.plot(new_x, new_y)
    plt.scatter(np.array(energy), np.array(log_psd))
    plt.plot()
    plt.show()