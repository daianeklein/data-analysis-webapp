import pandas as pd
import datetime

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from numpy import mean

import utilities as u
from dicts import dictionaries as d
from dicts import invert_dict as iv

class DataFiles:
    '''
    This class has all the methods to provide the necessary data to visualize the final output of 
the project.
It initializes data upon the creation of a new instance of that class, runs data cleaning,
creates the RFM table and clusters using K-Means algorithm.
    '''

    now = datetime.datetime.today().strftime('%Y-%m-%d')
    now = pd.to_datetime(now, format='%Y-%m-%d')

    def __init__(self,  user_files   = '/Users/daianeklein/Documents/DS/sam-media/data/users.csv',
                        transc_files = '/Users/daianeklein/Documents/DS/sam-media/data/transactions.tsv'):
        self.df_users = pd.read_csv(user_files, sep=',')
        self.df_transac = self.df_transac = pd.read_csv(transc_files, sep ='\t')
        self.df_transac = self.clean_dataset()

    def clean_dataset(self):
        '''
        This method runs basic data cleaning in transaction dataset
        '''
        for i in self.df_transac['pricepoint'].unique():
            if i != 3.6:
                self.df_transac.loc[self.df_transac['pricepoint'] > 3.6, 'pricepoint'] = 3.6
        self.df_transac['status'] = self.df_transac['status'].fillna('Failed')
        
        return self.df_transac
        
    def create_dataframes(self, status):
        '''
        This method merges both dataframes - users and transactions - and runs several transformations
        in order to create the final result.

        :param status: the value of status, Delivered or Failed
        :return: the final result - dataset for data visualization
        '''
        self.df = self.df_users.merge(self.df_transac, on = 'user_id', how = 'inner')
        self.df = self.df.drop(columns=({'phone_operator_y', 'service_x'}))
        self.df = self.df.rename(columns=({'phone_operator_x' : 'phone_operator', 
                        'service_y' : 'service'}))

        u.create_days_of_week(self.df, 'transaction_timestamp')

        dataframe = self.df[self.df['status'] == status]
        dataframe_rfm = self.create_rfm_table(dataframe)

        dataframe = dataframe.merge(dataframe_rfm, how = 'inner', left_on = 'user_id', right_index = True)
        selected_cols = ['user_id', 'phone_operator', 'os_name', 'affiliate', 
        'service', 'day_of_week', 'recency', 'frequency', 'pricepoint_sum']

        dataframe = dataframe[selected_cols]
        dataframe = dataframe.drop_duplicates()
        dataframe = dataframe.dropna()
        dataframe = dataframe.set_index('user_id')

        cols = ['phone_operator', 'service', 'day_of_week', 'affiliate', 'os_name']
        for i in dataframe[cols]:
            dataframe[i] = dataframe[i].map(d.dictionaries)

        if status == 'Failed':
            dataframe['frequency'] = dataframe['frequency']  *-1
            dataframe['pricepoint_sum'] = dataframe['pricepoint_sum'] *-1

        dataframe = self.change_recency_score(dataframe)
        dataframe['total_score'] = dataframe.sum(axis=1)
        dataframe['total_score'] = abs(dataframe['total_score'])
        dataframe = self.create_clusters(dataframe)

        return dataframe

    def change_recency_score(self, dataframe):
        '''
        This method creates a rank for the recency variable. According to the difference in days,
        the score can vary between 1 to 3. The 3 is the best one, whereas the 1 is the worse.

        :param: dataframe
        :return: a dataframe with recency column as a range between 1 to 3
        '''
        dataframe['recency'] = dataframe['recency'].apply(lambda x: 3 
                                     if x < 31 else 2
                                     if x > 30 and x < 61 else 1
                                     if x > 60 else 0)

        return dataframe

    def create_rfm_table(self, dataframe):
        '''
        This method creates the RFM table grouped by user ID.
        For recency, it considers the most recent day by the user.
        For frequency, it considers the count of delivered attempts by the user
        For the price point, which stands for the revenue, it considers the sum of each
        price point by user.

        :param: dataframe
        :return: a dataframe grouped by user ID with recency, frequency, and sum of price point
        '''
        dataframe['transaction_timestamp'] = dataframe['transaction_timestamp'].astype('datetime64')


        rfm = dataframe.groupby('user_id').agg({'transaction_timestamp': lambda x: ( self.now- x.max()).days,
                                    'user_id' : lambda x: len(x),
                                    'pricepoint': lambda x: x.sum()})

        rfm = rfm.rename(columns=({'transaction_timestamp' : 'recency',
                                    'user_id' : 'frequency',
                                    'pricepoint' : 'pricepoint_sum'}))
        
        rfm['pricepoint_sum'] = round(rfm['pricepoint_sum'], 2)

        return rfm

    def create_clusters(self, dataframe):
        '''
        This method creates the clusters using the algorithm K-Means.
        It provides a scaler transformation in the data, predicts each cluster, and creates a 
        column in the dataframe with it predictions.
        Note: The parameter n_cluster which stands for the number of the cluster the user is about
        to create is fixed in 3.

        :param: dataframe
        :return: a dataframe with an aditional column containing each cluster number
        '''
        scaler = StandardScaler()
        dataframe = dataframe.dropna()

        X = dataframe
        x_std = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters = 3, init = 'k-means++', random_state = 42)
        kmeans.fit(x_std)
        dataframe['cluster'] = kmeans.predict(x_std)

        return dataframe

        
