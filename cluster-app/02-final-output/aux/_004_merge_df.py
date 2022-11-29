import pandas as pd

transactions = pd.read_csv('/Users/daianeklein/Documents/DS/clusters-analysis-dash/data-analysis-webapp/cluster-app/03-data/transactions.csv')
users = pd.read_csv('/Users/daianeklein/Documents/DS/clusters-analysis-dash/data-analysis-webapp/cluster-app/03-data/users.csv')

df = users.merge(transactions, on = 'user_id', how = 'inner')
df = df.drop(columns=({'phone_operator_y', 'service_x'}))
df = df.rename(columns=({'phone_operator_x' : 'phone_operator', 
                        'service_y' : 'service'}))

df.to_csv('data.csv', index = False, sep = ';')


# print(users.head())