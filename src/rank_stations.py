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
with open("./data/flux_income_nearest.pkl", 'rb') as picklefile: 
    flux = pkl.load(picklefile)

"""
rank stations based on income and foot traffic
"""

#ranking subalgorithm
def weighting(income_in,flux_in):
    alpha = 0.8 # alpha is weighting factor [0 is all flux, 1 is all income]
    i_max_index, i_max = max(enumerate(income_in), key=operator.itemgetter(1))
    f_max_index, f_max = max(enumerate(flux_in), key=operator.itemgetter(1))
    i_weight = [alpha*(x/i_max) for x in income_in]
    f_weight = [(1-alpha)*(x/f_max) for x in flux_in]
    return [sum(x) for x in zip(i_weight,f_weight)]

# apply ranking to data
income_w = list(flux['INCOME'])
flux_w = list(flux['EXIT_SUM'])
ranks =  weighting(income_w,flux_w)
flux['RANK'] = ranks

# sort by rank
flux.sort_values('RANK',ascending=False).reset_index()

# save ranked data
with open('./data/rank.pkl', 'wb') as picklefile:
    pkl.dump(flux, picklefile)

