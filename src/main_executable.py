import os

"""
Runs all subprograms to load, parse, filter, and rank MTA foot traffic data
Each subroutine produces a subsequent pickle file to drive following subroutine
"""

# load and parse data
os.system(python load_parse.py)

# filter outliers from data
os.system(python filter_data.py)

# reduce data to foot traffic/day/station
os.system(python sum_by_station.py)

# load and parse census household income data
os.system(python build_income_location.py)

# geolocate stations
os.system(python build_station_location.py)

# map household income to stations
os.system(python map_income_to_stations.py)

# rank stations based on footfall and income
os.system(python rank_stations.py)