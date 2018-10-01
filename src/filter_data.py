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
import pickle file
"""
with open("./data/turnstile_data.pkl", 'rb') as picklefile: 
    flux = pkl.load(picklefile)

# Computing IQR

factor = 1.5

# filter for ENTRY outliers
filtered_entry = pd.DataFrame(columns=flux.columns)

# loop through stations
for station in flux.STATION.unique():

    current_station = flux[flux['STATION']==station]

    # quantile values for current station
    Q1 = current_station.ENTRY_FLUX.quantile(0.25)
    Q3 = current_station.ENTRY_FLUX.quantile(0.75)
    IQR = Q3 - Q1

    # Filtering Values between Q1-1.5IQR and Q3+1.5IQR
    mask = current_station.ENTRY_FLUX.between(Q1-IQR*factor, Q3+IQR*factor, inclusive=True)
    
    #pd.concat([filtered,current_station[mask]],axis=1)
    #filtered.concat(current_station[mask],ignore_index=True)
    filtered_entry = filtered_entry.append(current_station[mask])
    
# filter for EXIT outliers
filtered = pd.DataFrame(columns=flux.columns)

# loop through stations
for station in filtered_entry.STATION.unique():

    current_station = filtered_entry[filtered_entry['STATION']==station]

    # quantile values for current station
    Q1 = current_station.EXIT_FLUX.quantile(0.25)
    Q3 = current_station.EXIT_FLUX.quantile(0.75)
    IQR = Q3 - Q1

    # Filtering Values between Q1-1.5IQR and Q3+1.5IQR
    mask = current_station.EXIT_FLUX.between(Q1-IQR*factor, Q3+IQR*factor, inclusive=True)
    
    #pd.concat([filtered,current_station[mask]],axis=1)
    #filtered.concat(current_station[mask],ignore_index=True)
    filtered = filtered.append(current_station[mask])

with open('./data/filtered_data.pkl', 'wb') as picklefile:
    pkl.dump(filtered, picklefile)