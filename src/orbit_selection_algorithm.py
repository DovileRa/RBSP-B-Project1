import datetime
import datetime as dt
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import gc
import matplotlib.cm as cm

my_date = dt.date(2018, 1, 1)

df = pd.read_csv('2018-01-01.csv')

print(df["Position"].size, df.tail(1).index.item())

df.drop(df[df.Position < 2.7].index, inplace=True)
df.reset_index(drop=True, inplace=True)
print(df["Position"].size, df.tail(1).index.item())
count = df["energy"].count()
print(count)
#index of the turning point
tp = []
keep = []
lost = []

for i in range(0, count-3):



    position_1 = df.iloc[i]["Position"]
    position_2 = df.iloc[i+1]["Position"]
    position_3 = df.iloc[i + 2]["Position"]


    if (position_1 > position_2 < position_3) & (position_2 < 3):
        tp.append(i+1)
        print(position_2)
        keep.append(i+1)
    else:
        lost.append(i+1)
print(tp)

def timestamp (dt):
    dt = datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S.%f')
    epoch = datetime.datetime.utcfromtimestamp(0)
    return(dt - epoch).total_seconds()




segment_1 = df[(df.index < tp[0])]
segment_2 = df[(df.index >= tp[0]) & (df.index < tp[1])]
segment_3 = df[(df.index >= tp[1])]

print(segment_1)
print(segment_2)
print(segment_3)

segment_1_position = segment_1["Position"]
segment_1_error = segment_1["Total_Error"]
segment_1_time = segment_1["HOPE_time"].apply(timestamp)
segment_2_position = segment_2["Position"]
segment_2_error = segment_2["Total_Error"]
segment_2_time = segment_2["HOPE_time"].apply(timestamp)
segment_3_position = segment_3["Position"]
segment_3_error = segment_3["Total_Error"]
segment_3_time = segment_3["HOPE_time"].apply(timestamp)
ax = plt.axes(projection = "3d")
ax.scatter(segment_1_position, segment_1_error, segment_1_time, color="red")
ax.scatter(segment_2_position, segment_2_error, segment_2_time, color="green")
ax.scatter(segment_3_position, segment_3_error, segment_3_time, color="blue")

print(f'lost: {lost}')
print(f'keep: {keep}')
plt.show()




    #time = df["HOPE_time"]
    #error = df["Total_Error"]
    #position = df["Position"]



    #fig,axes = plt.subplots()
    #axes.scatter(time, position)
    #plt.show()