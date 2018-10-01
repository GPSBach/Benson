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
pd.set_option('display.max_rows', 50)

"""
load, parse, and initially sample data
"""
# function to load and concatanate sample data
# Source: http://web.mta.info/developers/turnstile.html
def get_data(week_nums):
    url = "http://web.mta.info/developers/data/nyct/turnstile/turnstile_{}.txt"
    dfs = []
    for week_num in week_nums:
        file_url = url.format(week_num)
        dfs.append(pd.read_csv(file_url))
    return pd.concat(dfs)

# load selected MTA data
week_nums = [180303, 180310, 180317, 180324, 180331, 180407,
 180414, 180421, 180428, 180505, 180512, 180519, 180526]
df = get_data(week_nums)

# convert weird style of control area name
df.rename(index=str, columns={"C/A":"CONTROL"},inplace=True)

# drop spurious data
df = df.drop(['LINENAME','DIVISION'], axis=1)

# filter out audits
df = df[df.DESC == 'REGULAR']

# drop the Description
df = df.drop(["DESC"], axis=1, errors="ignore")

# strip spurious whitespace from column names
df.columns = [column.strip() for column in df.columns]

# convert time data into datetime objects
df['TIMING'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'],format = '%m/%d/%Y %H:%M:%S' )"""
Convert data to daily flux vs turnstile for entries
"""

# sort values
df.sort_values(["CONTROL", "UNIT", "SCP", "STATION", "TIMING"], inplace=True, \
                          ascending=False)

# get first each day
daily_entries = df.groupby(["CONTROL", "UNIT", "SCP", "STATION", "DATE"])\
.ENTRIES.first().reset_index()

# make columns for previous day's data
daily_entries[["PREV_DATE", "PREV_ENTRIES"]] = (daily_entries
                                            .groupby(["CONTROL", "UNIT", "SCP", "STATION"])["DATE", "ENTRIES"]
                                            .transform(lambda grp: grp.shift(1)))
# drop first column
daily_entries.dropna(subset=["PREV_DATE"], axis=0, inplace=True)

# deal with negative data - from Lara's example
def get_daily_counts_entries(row, max_counter):
    counter = row["ENTRIES"] - row["PREV_ENTRIES"]
    if counter < 0:
        # Maybe counter is reversed?
        counter = -counter
    if counter > max_counter:
        #print(row["ENTRIES"], row["PREV_ENTRIES"])
        counter = min(row["ENTRIES"], row["PREV_ENTRIES"])
        # if current entries is bad, use yesterday's count as proxy
    if counter > max_counter:
        # Check it again to make sure we are not giving a counter that's too big
        return 0
    return counter

# If counter is > 1Million, then the counter might have been reset.  
# Just set it to zero as different counters have different cycle limits
daily_entries["ENTRY_FLUX"] = daily_entries.apply(get_daily_counts_entries, axis=1, max_counter=1000000)

"""
Convert data to daily flux vs turnstile for exits
"""

# get first each day
daily_exits = df.groupby(["CONTROL", "UNIT", "SCP", "STATION", "DATE"])\
.EXITS.first().reset_index()

# make columns for previous day's data
daily_exits[["PREV_DATE", "PREV_EXITS"]] = (daily_exits
                                            .groupby(["CONTROL", "UNIT", "SCP", "STATION"])["DATE", "EXITS"]
                                            .transform(lambda grp: grp.shift(1)))
# drop first column
daily_exits.dropna(subset=["PREV_DATE"], axis=0, inplace=True)

# deal with negative data - from Lara's example
def get_daily_counts_exits(row, max_counter):
    counter = row["EXITS"] - row["PREV_EXITS"]
    if counter < 0:
        # Maybe counter is reversed?
        counter = -counter
    if counter > max_counter:
        #print(row["EXITS"], row["PREV_EXITS"])
        counter = min(row["EXITS"], row["PREV_EXITS"])
        # if current entries is bad, use yesterday's count as proxy
    if counter > max_counter:
        # Check it again to make sure we are not giving a counter that's too big
        return 0
    return counter

# If counter is > 1Million, then the counter might have been reset.  
# Just set it to zero as different counters have different cycle limits
daily_exits["EXIT_FLUX"] = daily_exits.apply(get_daily_counts_exits, axis=1, max_counter=1000000)

"""
merge entries and exits into single dataframe
"""

# drop duplicate data
daily_entries.drop(['ENTRIES','PREV_ENTRIES','PREV_DATE'], axis=1, inplace=True)
daily_exits.drop(['EXITS','PREV_EXITS','PREV_DATE'], axis=1, inplace=True)

flux = pd.merge(daily_entries,daily_exits,on=['CONTROL','UNIT','SCP','STATION','DATE'])

"""
reconvert date into datetime object
"""

# convert time data into datetime objects
flux['TIMING'] = pd.to_datetime(flux['DATE'],format = '%m/%d/%Y')
flux.drop(['DATE'],axis=1,inplace=True)
flux.rename(index=str, columns={"TIMING":"DATE"},inplace=True)

"""
pickle output
"""

# write as binary ('wb')
with open('./data/turnstile_data.pkl', 'wb') as picklefile:
    pkl.dump(flux, picklefile)
