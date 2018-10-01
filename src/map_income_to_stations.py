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
import geopy.distance
import operator

"""
import data files
"""

# load station flux datafile
with open("./data/fluxsum_locations.pkl", 'rb') as picklefile: 
    flux = pkl.load(picklefile)
    
# load station locations
with open("./data/income.pkl", 'rb') as picklefile: 
    income = pkl.load(picklefile)

"""
assign nearest income data to each station
"""

bling_station = []
for f_index, f_row in flux.iterrows():
    dist = []
    bling = []
    for i_index, i_row in income.iterrows():
        if i_row['MEDIAN'] > 10:
            dist.append(geopy.distance.vincenty([f_row['LAT'],f_row['LON']],[i_row['LAT'],i_row['LON']]).m)
            bling.append(i_row['MEDIAN'])
    dist_index, dist_value = min(enumerate(dist), key=operator.itemgetter(1))
    bling_station.append(bling[dist_index])

"""
modify dataframe and save
"""
# modify data structure
flux["INCOME"]=bling_station 

with open('./data/flux_income_nearest.pkl', 'wb') as picklefile:
    pkl.dump(flux, picklefile)

