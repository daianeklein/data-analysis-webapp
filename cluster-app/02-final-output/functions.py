import pandas as pd
import datetime

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from numpy import mean

import utilities as u
#from dicts import dictionaries as d
#from dicts import invert_dict as iv

def create_days_of_week(dataframe, column):
    '''
    Creates the day of the week based on a datatetime column and 
    transforms from numbers to name of the day
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
    #return dataframe

