from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn import metrics

def linear_regression(x,y,verbose = False):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.2, random_state=0)

    regressor = LinearRegression()
    regressor.fit(x_train.reshape(-1,1), y_train)

    y_pred = regressor.predict(x_test.reshape(-1,1))

    intercept = regressor.intercept_
    gradient = regressor.coef_[0]
    #RMSE = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    RMSE = metrics.mean_squared_error(y_test, y_pred)

    if(verbose):
        print('intercept = ', intercept)
        print('gradient =', gradient)
        print('error =', RMSE)

    return gradient, intercept, RMSE






