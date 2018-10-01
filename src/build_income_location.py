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

# configuration options
%matplotlib inline
matplotlib.style.use("seaborn-muted")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 20)

"""
read in and parse national income data
"""
# read data
income = pd.read_csv('./data/income_national.csv', encoding = "ISO-8859-1")

# sort to NY and NY
income = income[(income['State_ab']=='NY') | (income['State_ab']=='NJ')]
income.reset_index()

# remove spurious data
income = income.drop(['id', 'State_Code', 'State_Name', 'State_ab', 'County', 'City', 'Place',
       'Type', 'Primary', 'Zip_Code', 'Area_Code', 'ALand', 'AWater', 'sum_w'], axis = 1)

# change column titles to caps
income.rename(index=str, columns={"Lat":"LAT"},inplace=True)
income.rename(index=str, columns={"Lon":"LON"},inplace=True)
income.rename(index=str, columns={"Mean":"INCOME"},inplace=True)
income.rename(index=str, columns={"Median":"MEDIAN"},inplace=True)
income.rename(index=str, columns={"Stdev":"STDEV"},inplace=True)

"""
write to save file
"""

income.to_csv('./data/income_locations.csv')

with open('./data/income.pkl', 'wb') as picklefile:
    pkl.dump(income, picklefile)