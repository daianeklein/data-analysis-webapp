import pandas as pd
import numpy as np
from numpy import random
import matplotlib.pyplot as plt


def create_days_of_week(dataframe, column):
    '''
    This function creates the day of the week based on a datatetime column.
    Then, to make it easier to visualize, using a dictionary, it transformns from numbers
    to name of the day.
    '''
    dataframe[column] = dataframe[column].astype('datetime64')
    dataframe['day_of_week'] = dataframe[column].dt.dayofweek

    days_of_week = {
        0 : 'monday',
        1 : 'tuesday',
        2 : 'wednesday',
        3 : 'thursday',
        4 : 'friday',
        5 : 'saturday',
        6 : 'sunday'
    }

    dataframe['day_of_week'] = dataframe['day_of_week'].map(days_of_week)
    return dataframe



def set_chart_config(title, xlabel, ylabel):
    '''
    This function operates global chart settings
    '''
    plt.title(title, fontsize = 12, pad = 10)
    plt.xlabel(xlabel, fontsize = 10)
    plt.ylabel(ylabel, fontsize = 10)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8);
    

def create_jitter_chart(dataframe, column, column2):
    '''
    This function creates a new column in the dataframe with sulfix "jitter". It's used to
    make the chart visualization better, specially the scatterplot by adding random noise
    to the observations in X and Y axis. Jitter technique does not modify the data values
    permanently or the data distribution.
    '''
    dataframe[column + '_jitter'] = random.randint(-4, 5, len(dataframe)) + dataframe[column]
    dataframe[column2 + '_jitter'] = random.randint(-4, 5, len(dataframe)) + dataframe[column2]
