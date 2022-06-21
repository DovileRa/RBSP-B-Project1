from src.linear_regression import linear_regression
from mageis_interface import mageisInterface
from hope_interface import hopeInterface
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

#instantiate dataclass
mageis = mageisInterface()
hope = hopeInterface()

#import data using function on class
hope.import_data()
mageis.import_data()

#extracting desired dataviews
hope_energy_series, hope_series = hope.flux_time()
mageis_energy_series , mageis_series = mageis.flux_time()
print(mageis_energy_series)

#removing low count values (HOPE energy values > 25keV)
low_count_index = np.where(hope_energy_series/1000 > 25)
hope_energy_series = np.delete(hope_energy_series,low_count_index)
hope_series = np.delete(hope_series,low_count_index)

#stitching the instrument data together to create one,continuous dataset
energy_series =np.append(hope_energy_series/1000, mageis_energy_series)
flux_series = np.append(hope_series,mageis_series)

#deleting all elements where the energy is too small for HOPE to detect (>15eV)
hope_invalid_index = np.where(energy_series < 0.15)
energy_series = np.delete(energy_series,hope_invalid_index)
flux_series = np.delete(flux_series,hope_invalid_index)

#deleting flux fill values
neg_flux_index = np.where(flux_series < 0)
flux_series = np.delete(flux_series,neg_flux_index)
energy_series = np.delete(energy_series,neg_flux_index)

# calculating phase space density
m = 9.1 * (10 ** -31)  # rest mass of an electron,kg
c = 3 * (10 ** 8)  # speed of light, ms^-1
phase_space_density = flux_series / (((energy_series ** 2) + 2 * (m) * (c ** 2) * (energy_series)) / (c ** 2))
neg_index = np.where(phase_space_density < 0)

phase_space_density = np.delete(phase_space_density,neg_index)
energy_series = np.delete(energy_series,neg_index )

plt.scatter(energy_series, np.log(phase_space_density))
plt.show()

#Linear Regression
log_energy_series = np.log(energy_series)
log_phase_space_density = np.log(phase_space_density)
gradient, intercept, RMSE = linear_regression(log_energy_series, log_phase_space_density, True)

plt.scatter(log_energy_series,log_phase_space_density)
plt.plot(list(range(-2,9)), [((gradient * energy_series) + intercept) for energy_series in range(-2,9)])
plt.vlines(x= 3.3, ymin= 0, ymax= 60, colors= 'red')
plt.plot
plt.show()

#Slicing algorithm

N = len(log_energy_series)

dataframe = pd.DataFrame(columns=['i','intercept_one', 'gradient_one', 'error_one', 'intercept_two', 'gradient_two', 'error_two','total_error'])
for i in range(0,N-6):

    series_one_energy = log_energy_series[0:4+i:1]
    series_one_psd = log_phase_space_density[0:4+i:1]
    gradient, intercept, RMSE = linear_regression(series_one_energy, series_one_psd, False)
    #plt.scatter(series_one_energy, series_one_psd, label='series one')
    #plt.plot(list(range(-2, 9)), [((gradient * energy_series) + intercept) for energy_series in range(-2, 9)])

    gradient_one = gradient
    intercept_one = intercept
    error_one = RMSE

    series_two_energy = log_energy_series[4+i:N:1]
    series_two_psd = log_phase_space_density[4+i:N:1]
    gradient, intercept, RMSE = linear_regression(series_two_energy, series_two_psd, False)

    gradient_two = gradient
    intercept_two = intercept
    error_two = RMSE

    total_error = (error_one + error_two)/2

    dataframe.loc[i, ['i']] = i
    dataframe.loc[i, ['intercept_one']] = intercept_one
    dataframe.loc[i, ['gradient_one']] = gradient_one
    dataframe.loc[i, ['error_one']] = error_one
    dataframe.loc[i, ['intercept_two']] = intercept_two
    dataframe.loc[i, ['gradient_two']] = gradient_two
    dataframe.loc[i, ['error_two']] = error_two
    dataframe.loc[i, ['total_error']] = total_error

print(dataframe)
print('the minimum error is', dataframe['total_error'].min())
dataframe['total_error'] = pd.to_numeric(dataframe['total_error'])
print('the index of the minimum error is', dataframe['total_error'].idxmin())

series_one_energy = log_energy_series[0:4+40:1]
series_one_psd = log_phase_space_density[0:4+40:1]
gradient, intercept, RMSE = linear_regression(series_one_energy, series_one_psd, False)
plt.scatter(series_one_energy, series_one_psd, label='HOPE')
plt.plot(list(range(-2, 9)), [((gradient * energy_series) + intercept) for energy_series in range(-2, 9)])


series_two_energy = log_energy_series[4+40:N:1]
series_two_psd = log_phase_space_density[4+40:N:1]
gradient, intercept, RMSE = linear_regression(series_two_energy, series_two_psd, False)
plt.scatter(series_two_energy, series_two_psd, label='MagEIS')
plt.plot(list(range(-2, 9)), [((gradient * energy_series) + intercept) for energy_series in range(-2, 9)])
#plt.vlines(x = 3.3, ymin= 0, ymax= 60, colors= 'red')
plt.legend()
plt.xlabel('log(Energy)')
plt.ylabel('log(Phase Space Density)')
plt.plot
plt.show()


position = hope.varget('L_star_Ele')
print('position =', position)

# plt.scatter(hope_energy_series/1000, hope_series, label = 'HOPE')
# plt.scatter(mageis_energy_series, mageis_series,label= 'MagEIS')
#
# plt.xscale('log')
# plt.yscale('log')
# plt.legend()
# plt.plot
# plt.show()
