
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[2]:

import numpy as np
import pandas as pd
data = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
data.head()


# In[3]:

data = data.drop('ID', axis = 1)
data = data.sort_values('Date')
data.head(3)


# In[4]:

data['Year'], data['Month-Date'] = zip(*data['Date'].apply(lambda x: (x[:4], x[5:])))
data = data[data['Month-Date'] != '02-29']


# In[5]:

temp_min = data[(data['Element'] == 'TMIN') & (data['Year'] != '2015')].groupby('Month-Date').aggregate({'Data_Value':np.min})
temp_max = data[(data['Element'] == 'TMAX') & (data['Year'] != '2015')].groupby('Month-Date').aggregate({'Data_Value':np.max})


# In[6]:

temp_min_2015 = data[(data['Element'] == 'TMIN') & (data['Year'] == '2015')].groupby('Month-Date').aggregate({'Data_Value': np.min})
temp_max_2015 = data[(data['Element'] == 'TMAX') & (data['Year'] == '2015')].groupby('Month-Date').aggregate({'Data_Value': np.max})


# In[7]:

min_broke = np.where(temp_min_2015['Data_Value'] < temp_min['Data_Value'])[0]
max_broke = np.where(temp_max_2015['Data_Value'] > temp_max['Data_Value'])[0]


# In[8]:

get_ipython().magic('matplotlib inline')
from matplotlib import pyplot as plt
plt.style.use('fivethirtyeight')
#The size 
plt.figure(num=None,figsize=(24,15),dpi=100,facecolor='w',edgecolor='k')
plt.plot(temp_min.values,'g', label = 'Record Low', ms = 20)
plt.plot(temp_max.values,'b', label = 'Record High', ms = 20)
plt.scatter(min_broke,temp_min_2015.iloc[min_broke], s = 70, label = 'Broken Low')
plt.scatter(max_broke,temp_max_2015.iloc[max_broke], s = 70, label = 'Broken High')
plt.xticks(range(0, len(temp_min), 20), temp_min.index[range(0, len(temp_min),20)], rotation = '45')
plt.gca().fill_between(range(len(temp_min)),temp_min['Data_Value'], temp_max['Data_Value'], alpha = 0.5)
plt.title('Record High and Low Temperatures(2005-2014) of Ann Arbor, Michigan, United States', size = 30)
plt.ylabel('Temperature (Tenths of Degrees C)',size = 30)
plt.xlabel('Day of the Year', size = 30)
plt.legend(loc = 'best', frameon = False)

#Signature Bar
plt.text(x=-16.0,y=-380,
    s = '   @Faizal, Faizal Azman                    Source: https://www.ncdc.noaa.gov/cdo-web/datasets  ',
    fontsize = 20, color = 'black', backgroundcolor = 'grey')


# In[ ]:



