from src.linear_regression import linear_regression
import numpy as np
import pandas as pd

def slicing_algorithm(energy, log_phase_space_density):

    N = len(energy)
    error_list = []
    grad_1_list = []
    grad_2_list = []
    in_1_list = []
    in_2_list = []

    dataframe = pd.DataFrame(columns=['i', 'intercept_one', 'gradient_one', 'error_one', 'intercept_two', 'gradient_two', 'error_two', 'total_error'])

    for i in range(0,N-5):

        series_one_energy = energy[0:3+i:1]
        series_one_psd = log_phase_space_density[0:3+i:1]
        gradient, intercept, RMSE = linear_regression(series_one_energy, series_one_psd, False)

        gradient_1 = gradient
        intercept_1 = intercept
        error_one = RMSE

        series_two_energy = energy[3+i:N:1]
        series_two_psd = log_phase_space_density[3+i:N:1]
        gradient, intercept, RMSE = linear_regression(series_two_energy, series_two_psd, False)

        gradient_2 = gradient
        intercept_2 = intercept
        error_two = RMSE
        error = (error_one + error_two)/2

        error_list.append(error)
        grad_1_list.append(gradient_1)
        grad_2_list.append(gradient_2)
        in_1_list.append(intercept_1)
        in_2_list.append(intercept_2)

        #dataframe.loc[i, ['i']] = i
        #dataframe.loc[i, ['intercept_one']] = intercept_1
        #dataframe.loc[i, ['gradient_one']] = gradient_1
        #dataframe.loc[i, ['error_one']] = error_one
        #dataframe.loc[i, ['intercept_two']] = intercept_2
        #dataframe.loc[i, ['gradient_two']] = gradient_2
        #dataframe.loc[i, ['error_two']] = error_two
        #dataframe.loc[i, ['total_error']] = error
    min_index = error_list.index(min(error_list))
    error = error_list[min_index]
    gradient_1 = grad_1_list[min_index]
    gradient_2 = grad_2_list[min_index]
    intercept_1 = in_1_list[min_index]
    intercept_2 = in_2_list[min_index]
    print(error_list)
    print('min error', error)

    return gradient_1, intercept_1, gradient_2, intercept_2, error
