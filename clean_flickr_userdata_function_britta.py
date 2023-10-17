import pandas as pd
import requests
from dotenv import load_dotenv
load_dotenv()
import os
import json
import flickrapi
import time
import numpy as np
import re
import pycountry


#df = df.loc[:,columns_to_keep]

def clean_user_data(df):
    df_user_data = df
    print(f'start cleaning, current shape is: {df_user_data.shape}' )
# defined columns to keep
    columns_to_keep=['person_id','person_ispro',
                    'person_username__content',
                    'person_location__content','person_photos_firstdatetaken__content',
                    'person_photos_firstdate__content','person_photos_count__content',
                    'person_timezone_label','person_timezone_offset',
                    'person_timezone_timezone_id']
# drop unnecessary columns
    df_user_data = df_user_data.loc[:,columns_to_keep]
# replace column names
    df_user_data.columns = df_user_data.columns.str.replace('person','user').str.replace('__content','')
# drop NaN values from location
    df_user_data = df_user_data.dropna(subset='user_location').reset_index(drop=True)
    print(f"shape after dropping NaN's is {df_user_data.shape}")
# change dtypes and lower string columns ( except user_id)
    df_user_data.user_ispro=df_user_data.user_ispro.astype('bool')
    df_user_data[['user_location','user_username','user_timezone_offset','user_timezone_timezone_id','user_timezone_label']] = df_user_data[['user_location','user_username','user_timezone_offset','user_timezone_timezone_id','user_timezone_label']].astype('string')
    df_user_data = df_user_data.apply(lambda x: x.str.lower() if x.dtype == "string" else x) 
    df_user_data.user_id=df_user_data.user_id.astype('string')
    df_user_data.user_photos_count = df_user_data.user_photos_count.astype('int')
    df_user_data.user_photos_firstdate = pd.to_datetime(df_user_data.user_photos_firstdate,unit='s',errors='coerce')
    df_user_data.user_photos_firstdatetaken = df_user_data.user_photos_firstdatetaken.astype('string')
    df_user_data.user_photos_firstdatetaken = pd.to_datetime(df_user_data.user_photos_firstdatetaken, dayfirst=True,format='%Y-%m-%d %H:%M:%S',errors='coerce')
    print(f'shape after basic cleaning is {df_user_data.shape}')
# rename dataframe and drop duplicates
    df_user_data_cleaned = df_user_data
    df_user_data_cleaned = df_user_data_cleaned.drop_duplicates(subset='user_id').reset_index(drop=True)
    print(f'shape after dropping duplicates {df_user_data_cleaned.shape}')

# split location column 
    columns_keep_temp = ['0','1','2']
    df_temp = df_user_data_cleaned.user_location.str.split(', ',expand=True)
    df_temp.columns = df_temp.columns.astype('string')
    df_temp = df_temp.loc[:, columns_keep_temp]
# merge new location columns to dataframe
    df_user_data_cleaned=pd.merge(df_user_data_cleaned,df_temp,left_index=True, right_index=True)

#replacing NaN with zero, bc Na is the country code for Namibia
    df_user_data_cleaned['0'] = df_user_data_cleaned['0'].replace(np.nan,'0')
    df_user_data_cleaned['1'] = df_user_data_cleaned['1'].replace(np.nan,'0')
    df_user_data_cleaned['2'] = df_user_data_cleaned['2'].replace(np.nan,'0')

# clean columns to find more matching values
    df_user_data_cleaned['0'] = df_user_data_cleaned['0'].str.lower().str.strip()
    df_user_data_cleaned['1'] = df_user_data_cleaned['1'].str.lower().str.strip()
    df_user_data_cleaned['2'] = df_user_data_cleaned['2'].str.lower().str.strip()

    return (df_user_data_cleaned)



    