import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import math


def get_Mar_Sept_frame():
    df = pd.read_csv('data_79_17.csv', index_col = 0)
    df['March_means'] = df.loc[:, '0301':'0331'].mean(axis=1)
    df['March_anomalies'] = df['March_means'] - df['March_means'].mean()
    df['September_means'] = df.loc[:, '0901':'0930'].mean(axis=1)
    df['September_anomalies'] = df['September_means'] - df['September_means'].mean()
    return df.loc[:, 'March_means':]

 


def get_ols_parameters(series):
    x = sm.add_constant(series.index.values)

    model = sm.OLS(series, x).fit()

    return [model.params["x1"], model.params["const"],
    model.rsquared, model.pvalues["x1"]]




def make_prediction(params, description = 'x-intercept:', x_name='x', y_name='y', ceiling=False):
    intercept = math.ceil(-params[1]/params[0]) if ceiling else -params[1]/params[0]
    print(description, intercept)
    print(str(round(params[2]*100)) + '% of variation in', y_name , 'accounted for by' , x_name , ('(linear model)'))
    print('Significance level of results:', str(round(params[3] * 100, 1))+'%')
    if params[3] <= 0.05:
        print('This result is statistically significant.')
    else:
        print('This result is not statistically significant.')



def make_fig_1(March_Sept_frame):
    march_parameters = get_ols_parameters(March_Sept_frame["March_means"])
    september_parameters = get_ols_parameters(March_Sept_frame["September_means"])
    ax = March_Sept_frame['March_means'].plot()
    March_Sept_frame['September_means'].plot()
    array = np.arange(1979, 2018)

    y = march_parameters[0] * array + march_parameters[1]
    y2 = september_parameters[0] * array + september_parameters[1]


    plt.plot(array, y)
    plt.plot(array, y2)

    ax.set_ylabel(r'NH Sea Ice Extent ($10^6$ $km^2$)', fontsize = 20)


def make_fig_2(March_Sept_frame):

    march_anomalies = get_ols_parameters(March_Sept_frame["March_anomalies"])
    september_anomalies = get_ols_parameters(March_Sept_frame["September_anomalies"])
    ax = March_Sept_frame['March_anomalies'].plot()
    y = March_Sept_frame['September_anomalies'].plot()

    array = np.arange(1979, 2018)


    y = march_anomalies[0] * array + march_anomalies[1]
    y2 = september_anomalies[0] * array + september_anomalies[1]


    plt.plot(array, y)
    plt.plot(array, y2)

    ax.set_ylabel(r'NH Sea Ice Extent ($10^6$ $km^2$)', fontsize = 20)

    plt.title('The Anomaly', fontsize =20)


#============


def main():

    df2 = get_Mar_Sept_frame()

    make_fig_1(df2)
    x = get_ols_parameters(df2["March_means"]) 
    make_prediction(x, description = 'Ice-free March in year', x_name='time', y_name='Artic sea ice', ceiling=True)
    plt.figure()


    make_fig_2(df2)
    y = get_ols_parameters(df2["September_means"])
    make_prediction(y, description = 'Ice-free September in year', x_name='time', y_name='Artic sea ice', ceiling=True)


    plt.show()
    








