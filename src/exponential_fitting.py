import datetime as dt
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import gc

my_date = dt.date(2018, 1, 1)
df = pd.read_csv('2018-01-01.csv')

df.drop(df[df.Position < 2.7].index, inplace=True)
count = df["energy"].count()
print(count)

parameters = []
error = []

# function that I am fitting
def func(x, a, b, c):
    return a/(b + np.power(x,c))

# iterates through one day of data and fits it with the above function
for i in range(0, count):
    energy = list(df.iloc[i]["energy"].split(" "))
    energy = list(map(float, filter(None, [s.strip("[").strip("]").strip("\n") for s in energy])))

    log_psd = list(df.iloc[i]["log_psd"].split(" "))
    log_psd = list(map(float, filter(None, [s.strip("[").strip("]").strip("\n") for s in log_psd])))

    initialParameters = np.array([1.0, 1.0, 1.0])
    fittedParameters, pcov = curve_fit(func, energy, log_psd, initialParameters)
    modelPredictions = func(energy, *fittedParameters)

    absError = modelPredictions - log_psd
    SE = np.square(absError)  # squared errors
    MSE = np.mean(SE)  # mean squared errors
    RMSE = np.sqrt(MSE)  # Root Mean Squared Error, RMSE
    Rsquared = 1.0 - (np.var(absError) / np.var(log_psd))

    parameters.append(fittedParameters)
    parameter_array = np.array(parameters)

    error.append(RMSE)
    error_array = np.array(error)

    print('Parameters:', fittedParameters)
    print('RMSE:', RMSE)
    print('R-squared:', Rsquared)
    print(i)

# Plots
    plt.xlim(0, 4000)
    plt.ylim(20, 60)
    xModel = np.linspace(min(energy), max(energy))
    yModel = func(xModel, *fittedParameters)

    plt.plot(xModel, yModel, color='red')
    plt.scatter(np.array(energy), np.array(log_psd))
    plt.xlabel('energy (KeV)')
    plt.ylabel('log(phase space density)')

    plt.savefig(f'data\exponential_fit_plots\ exponential_{my_date}_{i}.jpeg')
    plt.close('all')
    gc.collect()
    plt.plot()
    plt.show()

# saves parameters to CSV file
parameter_df = pd.DataFrame(parameter_array, columns=["a", "b", "c"])
parameter_df["Error"] = error_array
parameter_df["Time"] = df["HOPE_time"]
parameter_df["Position"] = df["Position"]

print(parameter_df)





