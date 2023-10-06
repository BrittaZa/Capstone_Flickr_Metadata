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

columns_to_keep=['person_id','person_ispro','person_path_alias',
                 'person_username__content','person_realname__content',
                 'person_location__content','person_photos_firstdatetaken__content',
                 'person_photos_firstdate__content','person_photos_count__content',
                 'person_timezone_label','person_timezone_offset',
                 'person_timezone_timezone_id']

columns_keep_temp = ['0','1','2']

df = df.loc[:,columns_to_keep]

def clean_user_data(df):

    df = df.loc[:,columns_to_keep]
    df_user_data_cleaned.columns = df_user_data_cleaned.columns.str.replace('person','user').str.replace('__content','')
    df_user_data_cleaned = df_user_data_cleaned.dropna(subset='user_location').reset_index(drop=True)
    df_user_data_cleaned.user_ispro=df_user_data_cleaned.user_ispro.astype('bool')
    df_user_data_cleaned[['user_location','user_realname','user_username','user_path_alias','user_timezone_offset','user_timezone_timezone_id','user_timezone_label']] = df_user_data_cleaned[['user_location','user_realname','user_username','user_path_alias','user_timezone_offset','user_timezone_timezone_id','user_timezone_label']].astype('string')
    df_user_data_cleaned = df_user_data_cleaned.apply(lambda x: x.str.lower() if x.dtype == "string" else x) 
    df_user_data_cleaned.user_id=df_user_data_cleaned.user_id.astype('string')
    # user_photos_count to int
    df_user_data_cleaned.user_photos_count = df_user_data_cleaned.user_photos_count.astype('int')
    df_user_data_cleaned.user_photos_firstdate = pd.to_datetime(df_user_data_cleaned.user_photos_firstdate,unit='s',errors='coerce')
    df_user_data_cleaned.user_photos_firstdatetaken = df_user_data_cleaned.user_photos_firstdatetaken.astype('string')
    df_user_data_cleaned.user_photos_firstdatetaken = pd.to_datetime(df_user_data_cleaned.user_photos_firstdatetaken, dayfirst=True,format='%Y-%m-%d %H:%M:%S',errors='coerce')

    user_in_df=[]
    df_user_data_cleaned = df_user_data_cleaned.drop_duplicates(subset='user_id')
    for i in df_user_data_cleaned.user_id.unique():
    user_in_df.append(i)

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

    # creating a new column empty column with NaN's
    df_user_data_cleaned['user_country']= np.nan
    df_user_data_cleaned['user_country_code'] = np.nan

    for index, row in df_user_data_cleaned.iterrows():
    zero = row['2']
    if pd.isna(row['user_country']):
        if zero in combined_dict:
            df_user_data_cleaned.at[index, 'user_country']= combined_dict[zero]

    for index, row in df_user_data_cleaned.iterrows():
    zero = row['1']
    if pd.isna(row['user_country']):
        if zero in combined_dict:
            df_user_data_cleaned.at[index, 'user_country']= combined_dict[zero]

    for index, row in df_user_data_cleaned.iterrows():
    zero = row['0']
    if pd.isna(row['user_country']):
        if zero in combined_dict:
            df_user_data_cleaned.at[index, 'user_country']= combined_dict[zero]