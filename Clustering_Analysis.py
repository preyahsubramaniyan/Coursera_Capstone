#!/usr/bin/env python
# coding: utf-8

# ## Clustering Analysis Project

# ## Part-1 ##

# **Firstly, installing required libraries**

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd


# **Secondly, scrape data set from Wikipedia website**

# In[2]:


# read the webpage from the wiki
url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
response = requests.get(url)
#Process and convert html data
data = response.text
soup = BeautifulSoup(data,'html.parser')
wiki_table=soup.find('table')
#develop dataframe
df = pd.read_html(str(wiki_table))[0]
df.head()


# **Thirdly, prepare the dataframe in pursuant of instructions**

# In[3]:


# Drop the first column
df.drop(0,inplace=True)
#Rename the columns names
df.columns = ['PostalCode','Borough','Neighborhood']
df.head()


# **Cleaning data as ignoring the rows which the "Borough" contains 'Not assigned'**

# In[5]:


#Remove "Borough" with 'Not assigned' values
df2=df[df['Borough'].str.contains("Not assigned") == False].reset_index()
df2.head()


# **Combine the rows into one row (and seperate with comma) which PostalCode and Borough as same value**

# In[6]:


df3= df2.groupby(['PostalCode', 'Borough'])['Neighborhood'].apply(', '.join).reset_index()
df3.head()


# **Get the number of rows of dataframe**

# In[7]:


df3.shape


# In[8]:


#Save data as'Capstone_part1.csv'
df3.to_csv('Capstone_part1.csv')
print('Successfully Saved!')


# ## Part - 2 ##

# **Firstly, installing required libraries**

# In[9]:


import pandas as pd


# **Secondly, get the geospatial Coordinates Data from https://cocl.us/Geospatial_data**

# In[10]:


# get the data and create the dataframe
url='https://cocl.us/Geospatial_data/Geospatial_Coordinates.csv'
df_geo=pd.read_csv(url)
df_geo.head()


# **Adjust the column name same as the first dataset**

# In[11]:


df_geo = df_geo.rename(columns = {'Postal Code':'PostalCode'}) 
df_geo.head()


# In[12]:


#We upload the first dataset where we save it as csv file in part 1
df3=pd.read_csv('Capstone_part1.csv')
df3.head()


# **Merge two dataframes based on the 'PostalCode' column**

# In[13]:


df3 = pd.merge(df3, df_geo, on = 'PostalCode')
df3.head()


# In[14]:


df3.shape


# In[15]:


#Save data as'Capstone_part2.csv'
df3.to_csv('Capstone_part2.csv', index=False)
print('Successfully Saved!')


# ## Part - 3 ##

# **Firstly, installing required libraries**

# In[16]:


import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import folium
import matplotlib.cm as cm
import matplotlib.colors as colors


# **Secondly, Upload the first dataset**

# In[17]:


#We upload the first dataset where we save it as csv file in part 2
df3=pd.read_csv('Capstone_part2.csv')
df3.head()


# **Thirdly, prepare the dataframe in pursuant of instructions**

# In[18]:


#We work with only "Borough" which contain the word Toronto 
df4=df3[df3['Borough'].str.contains('Toronto')]
df5=df4.reset_index(drop=True)
df5.head()


# In[19]:


df5.shape


# **For clustering the data, we can use the Borough as Label**

# In[20]:


# Learn the different value of Borough 
df5['Borough'].value_counts()


# In[21]:


# Create a new column as Label and get the date from 'Borough' as integer
df5['Label']=df5['Borough'].replace(to_replace=['Downtown Toronto','Central Toronto','West Toronto','East Toronto'],value=[1,2,3,4],inplace=False)
df5.head()


# **Fourthly, visualize the data**
# 
# Learn the coordinates of Toronto

# In[22]:


address = 'Toronto'
geolocator = Nominatim(user_agent="toronto_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(f'The geograpical coordinate of Toronto are {latitude}, {longitude}.')


# **Preparing to create the clustering map of Toronto**

# In[23]:


#for set the cluster number as label number
kclusters=len(df5.Label.unique())

# create map
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=11)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i + x + (i*x)**2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, cluster in zip(df5['Latitude'], df5['Longitude'], df5['Label']):
    label = folium.Popup(str(df5['Borough']) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_toronto)


# **Display the neighborhood map of Toronto with 4 clustering**

# In[24]:


map_toronto


# ## Thank You ##
