# Databricks notebook source
#!/usr/bin/env python
# coding: utf-8


# COMMAND ----------

# MAGIC %md # SAM MEDIA  CHALLENGE

# COMMAND ----------

# 
# 
# ***
# 
# Data Analysis techniques to identify potential patterns to maximize the number of successful billing attempts
# 
# ***


# COMMAND ----------

# MAGIC %md ## HOW THIS NOTEBOOK IS ORGANIZED

# COMMAND ----------


# **1.INTRODUCTION**
# 
#     Business Problem and methodology definition
# 
# **2. FUNCTIONS**
# 
#     Functions created to be used through the notebook/analysis
# 
# **3. LIBRARIES IMPORT**
#         
#     Necessary libraries import
# 
# **4. DATA IMPORT**
# 
#     Imported of both datasets
# 
# **5. DATASET OVERVIEW**
# 
#     Data type, missing values, possible errors
# 
# 
# **6. MERGE OF BOTH DATASETS**
# 
#     By 'user_id', a merge of both datasets
# 
# **7. DELIVERED TRANSACTIONS ANALYSIS**
# 
#     RFM table
#     Categorical Analysis
#     Overall score
# 
# **8. FAILED TRANSACTIONS ANALYSIS**
# 
#     RFM table
#     Categorical Analysis
#     Overall score
# 
# **9.CONCLUSION**
# 
#     Final considerations


# COMMAND ----------

# MAGIC %md ## METHODOLOGY

# COMMAND ----------


# We will use the CRISP-DM as the method for this analysis project.
# 
# CRISP-DM stands for "Cross-Industry Standard Process for Data Mining", very common for project management methods in Data Science.
# 
# Composed of six steps that together form a complete cycle, CRISP methodology shows a "360º project view".
# 
# For the purpose of this notebook, we won't go through each step (as ML modelling or deployment), but the idea remains the same: build a easy-undertanding framework which can be improve in every new started cycle.
# 
# The CRISP-DM Cycle:

# <img src="https://www.datascience-pm.com/wp-content/uploads/2018/09/crisp-dm-wikicommons.jpg" alt="CRISP-DM - Data Science Process Alliance" jsname="HiaYvf" jsaction="load:XAeZkd;" class="n3VNCb" data-noaft="1" width="400" height="500">


# COMMAND ----------

# MAGIC %md ## BUSINESS PROBLEM

# COMMAND ----------


# In June, the number of delivered billings has decreased over the day as we can see in the following line chart.

# <img style="display: block;-webkit-user-select: none;margin: auto;cursor: zoom-in;background-color: hsl(0, 0%, 90%);transition: background-color 300ms;" src="https://i.ibb.co/RPLXynY/delivered-billings.png" width="717" height="247">

# This analysis aims to identify opportunities to:
# 
# 1. Understand the data behavior
# 2. Analyze the variables which have the most impact on the delivered billings attempts
# 3. Find patterns in the users who have successfully been charged
# 4. Identify a method to improve the metrics of the users that have not been successfully charged


# COMMAND ----------

# MAGIC %md # FUNCTIONS

# COMMAND ----------




def set_chart_config(title, xlabel, ylabel):
    plt.title(title, fontsize = 12, pad = 10)
    plt.xlabel(xlabel, fontsize = 10)
    plt.ylabel(ylabel, fontsize = 10)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8);
    
    
def create_rfm_table(dataframe):
    now = datetime.datetime.today().strftime('%Y-%m-%d')
    now = pd.to_datetime(now, format='%Y-%m-%d')

    rfm = dataframe.groupby('user_id').agg({'transaction_timestamp': lambda x: ( now- x.max()).days,
                                 'user_id' : lambda x: len(x),
                                        'pricepoint': lambda x: x.sum()})

    rfm = rfm.rename(columns=({'transaction_timestamp' : 'recency',
                              'user_id' : 'frequency',
                              'pricepoint' : 'pricepoint_sum'}))
    #rfm = rfm.reset_index()
    rfm['pricepoint_sum'] = round(rfm['pricepoint_sum'], 2)

    return rfm


def create_viz_rfm(dataframe):
    
    rfm = create_rfm_table(dataframe)
    sns.set_theme()

    plt.figure(figsize = (15,5))
    plt.subplot(1, 3, 1)
    sns.histplot(data = rfm, x = 'recency', kde = True, color = 'cadetblue')
    set_chart_config('Histogram - Recency', '', '')

    plt.subplot(1, 3, 2)
    sns.histplot(data = rfm, x = 'frequency', color = 'cadetblue')
    set_chart_config('Histogram - Frequency', '', '')

    plt.subplot(1, 3, 3)
    sns.countplot(data = rfm, x = 'pricepoint_sum',palette = 'crest')
    set_chart_config('Barplot - Price Point (Sum)', '', '')
    plt.xticks(rotation = 90);

def change_recency_score(dataframe):
    dataframe['recency'] = dataframe['recency'].apply(lambda x: 3 
                                     if x < 31 else 2
                                     if x > 30 and x < 61 else 1
                                     if x > 60 else 0)
    return dataframe


def create_days_of_week(dataframe, column):
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



# COMMAND ----------

# MAGIC %md # IMPORTS

# COMMAND ----------




import pandas           as pd
import numpy            as np
import seaborn          as sns

from numpy import random
from numpy import mean

import matplotlib.pyplot as plt
import datetime

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

import invert_dict as d



# COMMAND ----------

# MAGIC %md # DATA IMPORT

# COMMAND ----------




users = pd.read_csv('../data/users.csv')
users.head()




transac = pd.read_csv('../data/transactions.tsv', sep = '\t', engine = 'python')
transac.head()



# COMMAND ----------

# MAGIC %md # DATASET OVERVIEW

# COMMAND ----------


# In this section, we're going to review the datatypes, presence of missing values, wrong records, etc.


# COMMAND ----------

# MAGIC %md ## DATA TYPES, MISSING VALUES, ETC.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md ### USERS DATASET

# COMMAND ----------




users.info()




users.shape




users.isna().sum()




len(users['user_id'].unique())




#looking for wrong dates
print(users['subscription_date'].max(), users['subscription_date'].min())
print(users['unsubscription_date'].dropna().max(), users['unsubscription_date'].dropna().min())




# investigating how the data is 'distribuited' among the variables
columns = ['phone_operator', 'os_name', 'os_version', 'affiliate',  'service', 'aggregator']

for i in users[columns]:
    print(users[i].value_counts())




#changind data type
users['subscription_date'] = users['subscription_date'].astype('datetime64')
users['unsubscription_date'] = users['unsubscription_date'].astype('datetime64')



# COMMAND ----------

# MAGIC %md ### TRANSACTIONS DATASET

# COMMAND ----------




transac.info()




transac.shape




transac.isna().sum()




len(transac['user_id'].unique())




# investigating how the data is 'distribuited' among the variables
columns = ['service', 'phone_operator', 'status', 'pricepoint']

for i in transac[columns]:
    print(transac[i].value_counts())




#looking for wrong dates
print(transac['transaction_timestamp'].max(), transac['transaction_timestamp'].min())




#looking for wrong pricepoint
print(transac['pricepoint'].max(), transac['pricepoint'].min())

transac[transac['pricepoint'] == 12345.6]




transac.loc[transac['pricepoint'] > 3.6, 'pricepoint'] = 3.6




print(transac['pricepoint'].max(), transac['pricepoint'].min())




# fill na values - once it's only 1 records, let's assume the most common value for this variable
transac['status'] = transac['status'].fillna('Failed')

transac.isna().sum()




#changing data type
transac['transaction_timestamp'] = transac['transaction_timestamp'].astype('datetime64')



# COMMAND ----------

# MAGIC %md # USERS & TRANSACTIONS

# COMMAND ----------


# After the data was cleaned, we're going to merge both dataframes: users and transactions.
# This is going to make our analysis easier.



print(len(users['user_id'].isin(transac['user_id'])), len(transac['user_id'].isin(users['user_id'])))
    




#merging two dataframes
df = users.merge(transac, on = 'user_id', how = 'inner')
df.shape




df.columns




df.isna().sum()




# there are 2 columns we have in both dataframes
# checking whether the values are the same
print(df[df['phone_operator_x'] != df['phone_operator_y']].shape)
print(df[df['service_x'] != df['service_x']].shape)




# column: phone_operator_x only 12 rows are different from each other.
# its pretty low, so let's assume the users table is the correct one
df = df.drop(columns=({'phone_operator_y', 'service_x'}))
df = df.rename(columns=({'phone_operator_x' : 'phone_operator',
                        'service_y' : 'service'}))

df.head(3)



# COMMAND ----------

# MAGIC %md ## DATA ANALYSIS - MERGED DATAFRAME

# COMMAND ----------


# Once both data frame is merged, in this section we're going to analyze the data.
# 
# Data analysis might be tricky sometimes, so we're going to use the following mind map as a guide. In its center there's the target variable, which is the Transaction variable and consequently the Price Point, then, there are all variables considered as dependents.
# 
# In other words, we listed all the variables that we considered to be strong enough to affect our target variable the most.
# 
# Note: Initially, these are some hypotheses. As we're going through the notebook and all the needed analysis we'll have the answers whether they are true or not.
# 
# 
# 
# 
# <img style="display: block;-webkit-user-select: none;margin: auto;cursor: zoom-in;background-color: hsl(0, 0%, 90%);transition: background-color 300ms;" src="https://i.ibb.co/p3rJChd/mind-map.png" width="717" height="449">
# 
# ***


# COMMAND ----------

# MAGIC %md ### SUBSCRIPTION DATE

# COMMAND ----------




df_subs = df.copy(deep = True)




create_days_of_week(df_subs, 'subscription_date')




df_subs['subscription_date'] = df_subs['subscription_date'].dt.strftime('%y-%m-%d')

sns.set_theme()
plt.figure(figsize = (15, 4))
aux = df_subs.groupby('subscription_date')['user_id'].count()
sns.lineplot(data = aux , color = 'teal')
set_chart_config('count of subscriptions by day', '', '')
plt.xticks(rotation = 90);




sns.set_theme()
plt.figure(figsize = (8, 3))

order = df_subs['day_of_week'].value_counts().to_frame().index
sns.countplot(data = df_subs, hue = 'day_of_week', x= 'day_of_week', order = order, palette = 'crest')
set_chart_config('count of subscriptions by day of the week', '', '')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);


# ***
# 
# 1. Looking at the count of subscriptions per day, we clearly see a decrease.
# 2. There're two peaks, both at the beginning of June.
# 3. Wednesday is the day which more users have signed
# 4. Thursday, on the other hand, is the day with fewer users subscribing.
# 5. There's also a really small value on June 23rd - possible an issue
# 
# ***


# COMMAND ----------

# MAGIC %md ###  UNSUBSCRIPTION DATE

# COMMAND ----------




# have unsubscripted
df_unsub = df_subs[~df_subs['unsubscription_date'].isna()]




#removing the hour, min and sec from our datetime columns
df_unsub = df_unsub.copy(deep = True)
df_unsub['subscription_date'] = pd.to_datetime(df_unsub['subscription_date'], format='%y-%m-%d')

df_unsub['unsubscription_date'] = df_unsub['unsubscription_date'].dt.strftime('%y-%m-%d')
df_unsub['unsubscription_date'] = pd.to_datetime(df_unsub['unsubscription_date'], format='%y-%m-%d')




# creating columns = days from subs to unsub
df_unsub['days_to_unsub'] = df_unsub['unsubscription_date'] - df_unsub['subscription_date']




df_unsub = df_unsub[['user_id', 'subscription_date', 'unsubscription_date', 'days_to_unsub']]




# removing duplicates
df_unsub = df_unsub.drop_duplicates()

# changing timedelta64[ns] type to float
df_unsub['days_to_unsub'] = df_unsub['days_to_unsub'].astype('timedelta64[D]')




df_unsub['days_to_unsub'].value_counts(normalize = True).to_frame()




sns.set_theme()
plt.figure(figsize = (6, 3))

sns.histplot(data = df_unsub, x ='days_to_unsub', bins = 10, color = 'cadetblue')
sns.despine(bottom = True, left = True)

set_chart_config('Days from subscription to unsubscription',
                'days',
                '')




mean_t = df_unsub['days_to_unsub'].mean()
median_t = df_unsub['days_to_unsub'].median()
mode_t = df_unsub['days_to_unsub'].mode()

print(f'Mean    {mean_t},\nMedian: {median_t}\nMode: {mode_t}')


# ***
# 
# 1. 64% of the users unsubscribe on the same day. 
# 2. 13% of the users unsubscribe after 14 days
# 3. The following days represent a small percentage of the data ( < 3%)
# 4. The median (0) also represents the high percentage of users unsubscribing right after subscribing.
# 
# ***


# COMMAND ----------

# MAGIC %md ### STATUS

# COMMAND ----------



# COMMAND ----------

# MAGIC %md #### PROPORTION OF DELIVERED x FAILED

# COMMAND ----------




# removing pending (we don't know which status is going to be)
df_status = df[df['status'] != 'Pending']




df_status['status'].value_counts(normalize = True)




delivered = df_status[df_status['status'] == 'Delivered'].groupby('user_id').count()[['status']].rename(columns=({'status' : 'delivered'}))
failed = df_status[df_status['status'] == 'Failed'].groupby('user_id').count()[['status']].rename(columns=({'status' : 'failed'}))




df_status_user = delivered.merge(failed, on = 'user_id')

df_status_user['proportion'] = round(df_status_user['failed'] / df_status_user['delivered'], 1)
df_status_user.head()




print(df_status_user['proportion'].mean())
print(df_status_user['proportion'].median())
print(df_status_user['proportion'].mode())




sns.set_theme()
plt.figure(figsize = (6, 3))

sns.histplot(data = df_status_user, x ='proportion', bins = 20, color = 'cadetblue')
sns.despine(bottom = True, left = True)

set_chart_config('Proportion of Failed x Delivered status by user',
                'Proportion',
                '')


# ***
# 
# The proportion of failed x delivered status is good:
#     
#     - Mean: 2.13
#     - Median: 1
# 
# The histogram chart shows that most of the data is concentrated between 0 and 1, which means that the company needs less than one attempt to successfully charge the user. The following table exemplifies this metric.
# 
# - First user: For 1 failed attempt, there're 3 successful
# 
# - Second user: for 2 failed attempts, there are 3 succesfully
# 
# - Third user: for 3 failed attempts, there're 5 successfully
# 
# | user_id | delivered| 	failed	| proportion |
# |-----    | -----    | -------  | ---------- |			
# |002f0e30f6da11ec98339db181f14dac|	3|	1|	0.3|
# |00307ca0f7bd11ec867b553062cb5bf9|	3|	2|	0.7|
# |006f74e0e44a11ecaa7033b4a0ee0e67|	5|	3|	0.6|
# 
# ***


# COMMAND ----------

# MAGIC %md #### BY STATUS, AFFILIATE AND SERVICE

# COMMAND ----------




sns.set_theme()
plt.figure(figsize = (15, 4))

plt.subplot(1, 3, 1)
sns.countplot(data = df_status, hue = 'status', x= 'status', palette = 'crest')
set_chart_config('status', '', '')

plt.subplot(1, 3, 2)
sns.countplot(data = df_status, hue = 'affiliate', x= 'affiliate', palette = 'crest')
set_chart_config('affiliate', '', '')

plt.subplot(1, 3, 3)
order = df_status['service'].value_counts().to_frame().index
sns.countplot(data = df_status, hue = 'service', x= 'service', order = order, palette = 'crest')
set_chart_config('service', '', '')


# ***
# 
# 1. 72% of the transactions are "Failed".
# 2. Affiliate aff_4 concentrates the majority of the data whereas affiliate aff_3 has quite a few
# 3. PS service is the most common one. The less common service is the GC
# 
# ***


# COMMAND ----------

# MAGIC %md # DELIVERED TRANSACTIONS

# COMMAND ----------


# ***
# 
# In this section, we're going to analyze all delivered transactions. By doing so, will be possible to set a pattern for users who have had successful transactions.
# 
# As we've said before, the main goal is to define what variables impact most in successful and not successful billings attempts.
# 
# ***



# creating dataframe
delivered = df.copy(deep = True)
delivered = delivered[delivered['status'] == 'Delivered']



# COMMAND ----------

# MAGIC %md ## RFM TABLE

# COMMAND ----------


# We're going to create a RFM table.
# 
# RMF stands for Recency, Frequency and Monetary value. These metrics have proven to be really effectivate predictor's to measure engagement and retention of customers.
# 
# **Recency**: How recently did the customer purchase from your company
# 
# **Frequency**: How often do your customers purchase in your store or visite your website
# 
# **Monetay**: How much do your customers spend in each visit ou purchase.



rfm = create_rfm_table(delivered)
rfm.head()




rfm['recency'].describe()




rfm['frequency'].describe()




rfm['pricepoint_sum'].describe()




create_viz_rfm(delivered)


# ***
# 
# 1. **Recency**
# The recency data seems to be a bimodal distribution. There're two clear peaks - around 30 days and roughly greater than 60. The second one concentrates on the majority of the users, which means most of them have been charged 2 months ago.
# 
# 
# 2. **Frequency**
# The frequency metric shows how many unique user has been charged. We can see that most of them are billed at one unique time. The second major group is the users with 3 successful billings attempts.
# 
# 
# 3. **Price Point**
# The price point sums up the amount billed for each user. Since the majority have a frequency equal to 1, consequently, the biggest price bar will be the first one.
# ***
# 


# COMMAND ----------

# MAGIC %md ### CATEGORICAL ANALYSIS

# COMMAND ----------


# Knowing our target variable (which is the Price Point), in this section, we're going to investigate how it is correlated to the categorical variables we've found important in the previous sections



create_days_of_week(delivered, 'transaction_timestamp')

# merging the rfm table
delivered = delivered.merge(rfm, how = 'inner', left_on = 'user_id', right_index = True)




#only categorical variables
cat_attributes = delivered.select_dtypes(exclude=['int64', 'float64'])

# adding pricepoint_sum - our target variable
cat_attributes = cat_attributes.merge(delivered[['pricepoint_sum', 'user_id']], how = 'left', on = 'user_id')




# target columns
cols = ['phone_operator', 'os_name', 'service', 'day_of_week', 'affiliate']

# data visualization
plt.figure(figsize=(18, 15))
x = 1

for i in cat_attributes[cols]:
    plt.subplot(3, 2, x)
    sns.boxplot(data = cat_attributes, x = i, y = 'pricepoint_sum', palette = 'crest')
    x += 1


# ***
# 
# 1. **Phone operator**
# The phone operator B seems the most profitable one, followed by operators C and A. In the general data, operator B is the most common one, but its median is the lowest one as well.
# 
# 
# 2. **OS name**
# Harmony is an outlier as we've seen at the beginning of the analysis, so, we're not going to consider it. The same for iPad and OSx. Between Android and IOS, Android users are more likely to have a successful charge. Its mean and median are greater than iOS
# 
# 
# 3. **Service**
# Most of the services look pretty similar. The TV is an exception as well as the median of PS. GC product seems to be the best one regarding profit.
# 
# 
# 4. **Day of Week**
# In the previous section, in all data, we've seen that Wednesday is the most common day for new subscriptions. It median also looks slightly higher than the other days. Sunday has the greatest superior limit. 
# 
# 
# 5. **Affiliate**
# There's a huge difference among the affiliates. aff_4 is by far the most profitable one. Something interesting is that aff_3 has way fewer subscriptions (in general data) and regarding profit, is also the last one.
# 
# ***
# 
# 


# COMMAND ----------

# MAGIC %md ### OVERALL SCORE

# COMMAND ----------


# According to the previous analysis, where we investigated the more common variables, the ones with more discrepancies, etc., based on all we've done and the business knowledge, we're going to attribute a score for each value.
# 
# This way will be possible to create an overall score, regardless of the variable type. Also, will be possible to standardize the whole dataset.



# removing columns and duplicates
delivered = delivered[['user_id', 'phone_operator', 'os_name', 'affiliate', 
        'service', 'day_of_week', 'recency', 'frequency', 'pricepoint_sum']]

delivered = delivered.drop_duplicates()

#removing NA
delivered = delivered.dropna()

delivered = delivered.set_index('user_id')




dictionaries = {
    'A' : 1,
    'B' : 3,
    'C' : 2,
    
    'Android'   : 2,
    'iOS'       : 1,
    'HarmonyOS' : 0,
    'iPadOS'    : 0,
    'OS X'      : 0,
    
    'gc' : 3,
    'cl' : 2,
    'ma' : 2,
    'ps' : 2,
    'tv' : 1,
    
    'monday'    : 2,
    'tuesday'   : 2,
    'wednesday' : 3,
    'thursday'  : 1,
    'friday'    : 2,
    'saturday'  : 3,
    'sunday'    : 2,

    'aff_3' : 1,
    'aff_2' : 2,
    'aff_4' : 3
}
    




delivered.head()




cols = ['phone_operator', 'service', 'day_of_week', 'affiliate', 'os_name']
for i in delivered[cols]:
    delivered[i] = delivered[i].map(dictionaries)




#creating a score for recency
change_recency_score(delivered)

# sum all columns - total score
delivered['total_score'] = delivered.sum(axis=1)
delivered['total_score'] = abs(delivered['total_score'])
delivered.head()



# COMMAND ----------

# MAGIC %md # FAILED TRANSACTIONS

# COMMAND ----------


# We've investigated all delivered transactions, so in this section, we'll analyze the failed transactions.
# 
# Based on the variables we do know that impact the main target and having transformed them from nominal to ordinal, we have a standard score, regardless of the type of the variable.


# COMMAND ----------

# MAGIC %md ## RFM TABLE

# COMMAND ----------




failed = df.copy(deep = True)
failed = failed[failed['status'] == 'Failed']




rfm = create_rfm_table(failed)




create_viz_rfm(failed)



# COMMAND ----------

# MAGIC %md ### OVERALL SCORE

# COMMAND ----------




create_days_of_week(failed, 'transaction_timestamp')

# merging the rfm table
failed = failed.merge(rfm, how = 'inner', left_on = 'user_id', right_index = True)




failed = failed[['user_id', 'phone_operator', 'os_name', 'affiliate', 'service', 
                 'day_of_week', 'recency', 'frequency', 'pricepoint_sum']]

failed = failed.drop_duplicates()

failed = failed.dropna()

failed = failed.set_index('user_id')




# failed['phone_operator'] = failed['phone_operator'].map(phone_operator)
# failed['service'] = failed['service'].map(service)
# failed['day_of_week'] = failed['day_of_week'].map(day_of_week)
# failed['affiliate'] = failed['affiliate'].map(affiliate)
# failed['os_name'] = failed['os_name'].map(os_name)

cols = ['phone_operator', 'service', 'day_of_week', 'affiliate', 'os_name']
for i in failed[cols]:
    failed[i] = failed[i].map(dictionaries)




change_recency_score(failed)




# once we're working with failed billings attempts, there's no sense in sum these variables
# i.e frequency for failed attemps means that as this number is higher, worst it is
# that's why we're changing them to negative

#failed['recency'] = failed['recency'] * -1
failed['frequency'] = failed['frequency']  *-1
failed['pricepoint_sum'] = failed['pricepoint_sum'] *-1

# sum all columns - total score
failed['total_score'] = failed.sum(axis=1)
failed['total_score'] = abs(failed['total_score'])
failed.head()



# COMMAND ----------

# MAGIC %md ## K-MEANS

# COMMAND ----------


# For this step, we're going to use K-Means, an unsupervised machine learning algorithm.
# 
# Knowing all the scores, important variables, frequency, recency, the sum of price points per user, etc., we're going to separate our data into 3 clusters. This way will be possible to understand, by the distance of each data point, how our users are grouped and then, we can move forward to plan action.


# COMMAND ----------

# MAGIC %md ## ELBOW METHOD

# COMMAND ----------


# The elbow method is used to determine the optimal number of clusters in k-means clustering.
# 
# Note: Although it's a very useful and common method, is up to the business decision the optimal number of clusters



scaler = StandardScaler()
failed = failed.dropna()

X = failed
x_std = scaler.fit_transform(X)

x_std




sns.set_theme()

wcss = []

for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init= 'k-means++', random_state = 0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
    
plt.plot(range(1, 11), wcss, color = 'cadetblue')
set_chart_config('Elbow Method', '', '')




kmeans = KMeans(n_clusters = 3, init = 'k-means++', random_state = 42)

kmeans.fit(x_std)
failed['cluster'] = kmeans.predict(x_std)

centroids = kmeans.cluster_centers_



# COMMAND ----------

# MAGIC %md ## CLUSTERS VISUALIZATION

# COMMAND ----------




failed = failed.copy(deep = True)

failed['pricepoint_sum_jitter'] = random.randint(-4, 5, len(failed)) + failed['pricepoint_sum']
failed['total_score_jitter'] = random.randint(-4, 5, len(failed)) + failed['total_score']




m1 = failed['total_score'].mean()
m2 = delivered['total_score'].mean()

fig3 = plt.figure(constrained_layout=True);
fig3 = plt.figure(figsize=(15,10));

gs = fig3.add_gridspec(2, 3) ## number of charts
fig3.add_subplot(gs[1, :]) ##chart 1

ax1 =sns.histplot(data = failed['total_score'], color = 'teal', label = 'failed')
med1 = plt.vlines(x=m1, linewidth=2, color='#d62728', ymin=0, ymax=1200, linestyle='--', 
                label = 'Median Failed')
ax = sns.histplot(data = delivered['total_score'], color = 'midnightblue', label = 'delivered')
med2 = plt.vlines(x=m2, linewidth=2, color='orange', ymin=0, ymax=1200, linestyle='--', 
                label = 'Median Delivered')

set_chart_config('Total Score: Delivered x Failed', 'Total Score', ' ')
plt.xticks(color = 'grey', fontsize = 8);
plt.yticks(color = 'grey', fontsize = 8);
plt.legend();

fig3.add_subplot(gs[0, :-1])
ax1 = sns.scatterplot(data = failed, x='pricepoint_sum_jitter', y = 'total_score_jitter', hue = 'cluster',
                    palette = {0 : 'midnightblue', 1 : 'mediumseagreen', 2 : 'darkturquoise'})
                   
set_chart_config('Cluster visualization - Failed Attempts', '', '')
plt.xticks(color = 'white');
plt.yticks(color = 'white');

fig3.add_subplot(gs[0, 2])
order = failed.groupby('cluster')['total_score'].mean().sort_values(ascending = False).index
ax3 = sns.barplot(data = failed, x = 'cluster', y = 'total_score',  estimator=mean,  order = order,
                 palette = {0 : 'midnightblue', 1 : 'mediumseagreen', 2 : 'darkturquoise'}, ci= False)

set_chart_config('Mean of Total Score by Cluster\nFailed Attempts', 'Cluster', '');


# ***
# 
# 1. For the first chart, we have a scatterplot with 3 groups generated using K-means algorithm. By having this visualization (handing the dataset with the customer ID as well), it's possible to address the best business decisions.
# 
# 
# 2. In The second chart there's a barplot comparing the mean of the total score for each cluster. As an initial analysis, we can have a big picture of the most, middle, and less important clusters based on the total score we've set before. Using the CRISP-DM methodology, we can dig into each cluster and have more information.
# 
# 
# 3. In the third chart, the histogram plot, we can compare the Total Score between the users who have had the delivered billing and the ones that haven't (failed). These two charts show how these two groups are different from each other, in number of users and also the total score. The goal is to maximize the delivered chart and consequently, decrease the failed one.
# 


# COMMAND ----------

# MAGIC %md ## FINAL DATAFRAME

# COMMAND ----------


# ***
# 
# Exporting the final dataframe of failed delivered, by user, with cluster number for each record.



#target columns
failed_export = failed[['phone_operator', 'os_name', 'affiliate', 'service', 'day_of_week',
       'recency', 'frequency', 'pricepoint_sum', 'total_score', 'cluster']]

# transforming negative values
failed_export = failed_export.abs()




# changing back to categorical variables
failed_export['phone_operator'] = failed_export['phone_operator'].map(d.phone_operator)
failed_export['os_name'] = failed_export['os_name'].map(d.os_name)
failed_export['service'] = failed_export['service'].map(d.service)
failed_export['day_of_week'] = failed_export['day_of_week'].map(d.day_of_week)
failed_export['affiliate'] = failed_export['affiliate'].map(d.affiliate)

failed_export

