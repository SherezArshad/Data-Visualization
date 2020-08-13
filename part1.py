

#Dealing with data that is stored on disk in csv format using pandas. 



from ftplib import FTP
import pandas as pd
from datetime import datetime
import numpy as np


def get_data():

    filename = 'N_seaice_extent_daily_v3.0.csv'

    df = pd.read_csv(filename, skiprows = 2, names = [0, 1, 2, 'Extent'], usecols=[0, 1, 2 ,3], parse_dates={'Dates': [0, 1, 2]})

    JD = pd.Series(data = df['Extent'].values, index = df['Dates'].values)

    sm = pd.date_range(JD.index[0], JD.index[-1])


    JD = JD.reindex(sm)
    
    return JD


def clean_data(JD):


    ey = pd.isnull(JD)  #new values (True and False)

    for i in range(len(JD)):
        if ey.iloc[i]:
            JD.iloc[i] = (JD.iloc[i - 1] + JD.iloc[i + 1]) / 2 # getting average

    ey = pd.isnull(JD)


    for i in range(len(JD)):
        if ey.iloc[i]:
            JD.iloc[i] = (JD.iloc[i - 365] + JD.iloc[i + 366]) / 2





def get_column_labels():

    lst = []
    for i in range(1, 13):
        if i == 2:
            last = 29
        elif i in [4, 6, 9, 11]:
            last = 31
        else:
            last = 32
        for j in range(1, last):
            lst.append(str(i).zfill(2) + str(j).zfill(2))

    return lst


def extract_df(JD):
    df = pd.DataFrame(index = list(range(1979, 2018)), columns =get_column_labels(), dtype = np.float64)
    for year in df.index:
        for mmdd in df.columns:
            df.loc[year,mmdd] = JD[datetime(year, int(mmdd[:2]), int(mmdd[2:]))]
    return df


def extract_2018(JD):
    return JD.loc[datetime(2018, 1, 1):]


def main():
    dat = get_data()
    clean_data(dat)
    df = extract_df(dat)
    df.to_csv('data_79_17.csv')
    extract_2018(dat).to_csv('data_2018.csv')

    

