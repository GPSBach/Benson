"""
Set Options
"""

# import libraries
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import pickle as pkl

"""
import data files
"""

# load filtered datafile
with open("./data/filtered_station.pkl", 'rb') as picklefile: 
    filtered_data = pkl.load(picklefile)

# load station locations
station_loc = pd.read_csv('./data/latlon_map.csv')

"""
parse lat lon data
"""

# format strings
locations = station_loc.LOCATION
locations = locations.str.replace(',',' ')
locations = locations.str.replace('(',' ')
locations = locations.str.replace(')',' ')
locations = locations.str.split()

# convert to float and append to data structure
lons = []
lats = []

for l in locations:
    lons.append(float(l[1].strip()))
    lats.append(float(l[2].strip()))
    
lons_pd = pd.Series(lons)
lats_pd = pd.Series(lats)
station_loc['LAT'] = lats_pd
station_loc['LON'] =  lons_pd

# remove spurious datas
station_loc = station_loc.drop('LOCATION', axis=1)

"""
pickle output
"""

# write as binary ('wb')
with open('./data/station_locations.pkl', 'wb') as picklefile:
    pkl.dump(station_loc, picklefile)