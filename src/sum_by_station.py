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
with open("./data/filtered_data.pkl", 'rb') as picklefile: 
    filtered = pkl.load(picklefile)

"""
apply aggregation function to get total fluxes per station
"""

# aggregate on station sum over all days
filtered_station = filtered.groupby(['STATION']).agg({'ENTRY_FLUX':['sum'], 'EXIT_FLUX' : ['sum']})
filtered_station.columns = filtered_station.columns.map('_'.join)

# resets index
filtered_station = filtered_station.sort_values(['EXIT_FLUX_sum'], ascending = False).reset_index()

# renames columns to be consistent
filtered_station.rename(index=str, columns={'ENTRY_FLUX_sum':"ENTRY_SUM"},inplace=True)
filtered_station.rename(index=str, columns={'EXIT_FLUX_sum':"EXIT_SUM"},inplace=True)

"""
write to save file
"""

with open('./data/filtered_station.pkl', 'wb') as picklefile:
    pkl.dump(filtered_station, picklefile)