import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_column_labels():

    return pd.date_range('2018-01-01', '2018-12-31').strftime('%m%d').tolist()

def get_2018():

    df = pd.read_csv('data_2018.csv', header = None)
    index = get_column_labels()
    index = index[:index.index('0916') + 1]
    series = pd.Series(df[1].values, index)
    return series


def extract_fig_1_frame(df):
    df2_index = ['mean', 'two_s']
    df2 = pd.DataFrame(index = df2_index, columns =df.columns)
    df2.loc['mean'] = df.mean()
    df2.loc['two_s'] = 2 * df.std(ddof=1)
    return df2

def extract_fig_2_frame(df):
    lst = [[], [], [], []]
    index = ['1980s', '1990s', '2000s', '2010s']
    df_rec = pd.DataFrame(index = index, columns = df.columns)
    df_rec.loc['1980s'] = df.loc[1980:1989].mean()
    df_rec.loc['1990s'] = df.loc[1990:1999].mean()
    df_rec.loc['2000s'] = df.loc[2000:2009].mean()
    df_rec.loc['2010s'] = df.loc[2010:2017].mean()
    return df_rec


def make_fig_1(fig1, frame5):
    fig1.loc['mean'].plot(label = 'mean')
    frame5.loc[2012].plot(label = '2012', linestyle = '--')
    get_2018().plot(label = '2018')


    lst = ['0000', '0101', '0220', '0411', '0531', '0720', '0908', '1028', '1217']
    Axes = plt.gca()
    Axes.set_xticklabels(lst)


    fig1.loc['mean']
    fig1.loc['two_s']

    lst3 = np.arange(365)


    tra = (fig1.loc['mean'] + fig1.loc['two_s']).values.astype(float)
    dan = (fig1.loc['mean'] - fig1.loc['two_s']).values.astype(float)


    Axes.fill_between(lst3, tra, dan, color = 'lightgrey', label = r'$\pm$2 std devs')
    Axes.legend(loc = 'upper right')

    Axes.set_ylabel(r'NH Sea Ice Extent ($10^6$ $km^2$)', fontsize = 20)


    plt.show()

def make_fig_2(fig2, frame5):

    
    fig2.loc['1980s'].plot(label = '1980s', linestyle = '--')
    fig2.loc['1990s'].plot(label = '1990s', linestyle = '--')
    fig2.loc['2000s'].plot(label = '2000s', linestyle = '--')
    fig2.loc['2010s'].plot(label = '2010s', linestyle = '--')
    get_2018().plot(label = '2018')


    lst = ['0000', '0101', '0220', '0411', '0531', '0720', '0908', '1028', '1217']
    Axes = plt.gca()
    Axes.set_xticklabels(lst)

    Axes.legend(loc = 'lower left')

    Axes.set_ylabel(r'NH Sea Ice Extent ($10^6$ $km^2$)', fontsize = 20)

    


    plt.show()




def main():
    df = pd.read_csv('data_79_17.csv', index_col = 0)

    graph = extract_fig_1_frame(df)
    make_fig_1(graph, df)


    graph = extract_fig_2_frame(df)
    make_fig_2(graph, df)


