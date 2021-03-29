
import requests
import pickle
import datetime
#!/usr/bin/env python

import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.smgov.net", 'gh0PGNOdsbpE9OEaUFU2DW2Y2')

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.smgov.net,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("ng8m-khuz", limit=50000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df['date_time']=pd.to_datetime(results_df['date_time'])
results_df['date']=results_df['date_time'].apply(lambda x: x.date())

results_df.sort_values(by='date_time')
lots_to_keep=['Structure 5','Structure 1','Lot 4 South','Structure 2','Structure 3','Structure 6','Structure 8','Structure 9','Structure 7']
results_df=results_df[results_df['lot_name'].apply(lambda x: x in lots_to_keep)]
results_df['available_spaces']=results_df['available_spaces'].apply(lambda x: int(x))

#look at the parking in the peak hours
peak_parking_av=results_df[results_df['date_time'].apply(lambda x: True if x.hour>=9 and x.hour<=20 else False)].groupby(by=['date']).mean()['available_spaces'].reset_index()

#look at the parking in the morning hours
morning_parking_av=results_df[results_df['date_time'].apply(lambda x: True if x.hour>=2 and x.hour<9 else False)].groupby(by=['date']).mean()['available_spaces'].reset_index()
morning_parking_av=morning_parking_av.rename(columns={"date": "date", "available_spaces": "TAKEN"})

joined_parking_df=peak_parking_av.set_index('date').join(morning_parking_av.set_index('date'),lsuffix='date',rsuffix='date').reset_index().sort_values(by='date')

joined_parking_df['NET PEAK SPOTS']=joined_parking_df['available_spaces']-joined_parking_df['TAKEN']
joined_parking_df['NET PEAK SPOTS']=joined_parking_df['NET PEAK SPOTS']+245
joined_parking_df=joined_parking_df[['date','NET PEAK SPOTS']].sort_values(by=['date'])

joined_parking_df[['date','NET PEAK SPOTS']].to_pickle('scraped_parking_data.pkl')