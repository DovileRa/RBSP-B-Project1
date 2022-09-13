import datetime as dt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

parameters = []
error = []
date = []
time = []
position = []
mlt = []
energy_array = []
log_psd_array = []

for j in range(1, 32):

    my_date = dt.date(2018, 1, j)
    df = pd.read_csv(f'{my_date}.csv')
    print(df)
    df.drop(df[df.Position < 2.7].index, inplace=True)
    count = df["energy"].count()
    print(df)
    print(count)

    # function that I am fitting
    def func(x, a, b, c):
        return a/(b + np.power(x, c))

    # iterates through one day of data and fits it with the above function
    for i in range(0, count):
        energy = list(df.iloc[i]["energy"].split(" "))
        energy = list(map(float, filter(None, [s.strip("[").strip("]").strip("\n") for s in energy])))

        log_psd = list(df.iloc[i]["log_psd"].split(" "))
        log_psd = list(map(float, filter(None, [s.strip("[").strip("]").strip("\n") for s in log_psd])))

        initialParameters = np.array([300.0, 5.0, 0.5])
        fittedParameters, pcov = curve_fit(func, energy, log_psd, initialParameters, maxfev=5000)
        modelPredictions = func(energy, *fittedParameters)

        absError = modelPredictions - log_psd
        SE = np.square(absError)  # squared errors
        MSE = np.mean(SE)  # mean squared errors
        RMSE = np.sqrt(MSE)  # Root Mean Squared Error, RMSE
        Rsquared = 1.0 - (np.var(absError) / np.var(log_psd))

        time.append(df.iloc[i]["HOPE_time"])

        position.append(df.iloc[i]["Position"])
        mlt.append(df.iloc[i]["MLT"])
        energy_array.append(df.iloc[i]["energy"])
        log_psd_array.append(df.iloc[i]["log_psd"])
        #energy.append((energy))     #(df.iloc[i]["energy"])
        #log_psd.append(log_psd)      #(df.iloc[i]["log_psd"])

        parameters.append(fittedParameters)
        parameter_array = np.array(parameters)

        error.append(RMSE)
        error_array = np.array(error)

        date.append(my_date)


        print('Parameters:', fittedParameters)
        print('RMSE:', RMSE)
        print('R-squared:', Rsquared)
        print(i)
        print("day:", j)


    parameter_df = pd.DataFrame(parameter_array, columns=["a", "b", "c"])
    parameter_df["Error"] = error_array
    parameter_df["Time"] = time
    parameter_df["Position"] = position
    parameter_df["Date"] = date
    parameter_df["MLT"] = mlt
    parameter_df["Energy"] = energy_array#pd.concat([parameter_df,df["energy"]],axis=1)
    parameter_df["log_PSD"] = log_psd_array #pd.concat([parameter_df, df["log_psd"]], axis=1)







print(parameter_df)
parameter_df.to_csv(f'exponential_params_01_2018.csv', index=True)






########################################################################################################################
    # Plots
#from matplotlib import pyplot as plt
#import gc
        #plt.xlim(0, 4000)
        #plt.ylim(20, 60)
        #xModel = np.linspace(min(energy), max(energy))
        #yModel = func(xModel, *fittedParameters)

        #plt.plot(xModel, yModel, color='red')
        #plt.scatter(np.array(energy), np.array(log_psd))
        #plt.xlabel('energy (KeV)')
        #plt.ylabel('log(phase space density)')

        #plt.savefig(f'data\exponential_fit_plots\ exponential_{my_date}_{i}.jpeg')
        #plt.close('all')
        #gc.collect()
        #plt.plot()
        #plt.show()

    # saves parameters to CSV file


