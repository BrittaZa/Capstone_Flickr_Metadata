# Python modules
import flickrapi
import pandas as pd
import requests
import json
import time
import os
from datetime import date
from datetime import datetime
import googlemaps
import random


# Keys needed for API access
api_key = '8eda6fcb3fd5a4de7b5714cd109221ca'
api_secret = '8d63ce31d49cdfae'
maps_api_key = 'AIzaSyDVshHcFqhGk9mSwT_lZtfzsfYeaF9ND2k'

# Configure maps access
gmaps = googlemaps.Client(key=maps_api_key)

# Flickr API object
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# Data directory used to store CVS files
data_dir = './data/'

def df_remove_dupes(df):
    len_before = len(df)
    df = df.drop_duplicates(ignore_index=False)
    len_after = len(df)
    print(f'Found {len_before - len_after} duplicates. Dataframe is now {len(df)} rows long.')
    return df

# Define the dataframes and lists with columns

df_photo_ids = pd.DataFrame(columns = ['id', 
                                       'owner', 
                                       'secret', 
                                       'title', 
                                       'ispublic'])

columns_df_photo_exif = ['id', 'Image Width', 'Image Height', 'Compression', 'Make', 'Model',
       'Orientation', 'Software', 'Date and Time (Modified)', 'Exposure',
       'Aperture', 'ISO Speed', 'Date and Time (Original)',
       'Date and Time (Digitized)', 'Flash', 'Focal Length', 'White Balance',
       'owner', 'secret', 'title', 'lat', 'lon', 'acc', 'country', 'admin_lvl1', 'admin_lvl2', 'city']

df_photo_exif = pd.DataFrame(columns = columns_df_photo_exif)

# Get some nice random words from an API

languages = ['en', 'it', 'de', 'es']

URL='https://random-word-api.herokuapp.com/word?number='

def get_words(number, length):
    response = requests.get(URL + str(number) + '&length=' + str(length) + '&lang=' + random.choice(languages)).text
    return json.loads(response)
    #return ['a', 'e', 'u']
    
# We want to run this script until we quit it manually
while True:
    try:
        # Iterate through words, query API for results containing this word, add to dataframe
        df_exif = pd.read_csv(data_dir + 'df_photo_exif_final.csv', index_col=[0])

        df_photo_ids = pd.DataFrame(columns = ['id', 
                                       'owner', 
                                       'secret', 
                                       'title', 
                                       'ispublic'])

        # start timer
        start_time = time.time()

        # count the number of added entries
        counter = 0

        for word in get_words(1, random.choice(range(3,5))):

            print(word)

            try:
                get_photos = flickr.photos.search(text = word,
                                privacy_filter = 1, 
                                content_types = 0,
                                page = 1,
                                per_page = 500,
                                has_geo = 1)
            except flickrapi.exceptions.FlickrError as ex:
                print("Error code: %s" % ex.code)
            
            for photo in get_photos.get('photos').get('photo'):
                df_photo_ids.loc[len(df_photo_ids)] = {'id': photo.get('id'), 
                                                    'owner': photo.get('owner'),
                                                    'secret': photo.get('secret'),
                                                    'title': photo.get('title'),
                                                    'ispublic': photo.get('ispublic')}
                counter += 1
            
        # end the timer and calculate duration
        end_time = time.time()
        minutes, seconds = divmod(int(end_time - start_time), 60)

        #print(f'Fetched {counter} entries in {minutes} minutes and {seconds} seconds. Dataframe is now {len(df_photo_ids)} rows long.')

        # Remove duplicates
        df_photo_ids = df_remove_dupes(df_photo_ids)

        # Look for ids that are in the exif file already (and drop them)
        length_before = len(df_photo_ids)
        df_photo_ids = df_photo_ids[~df_photo_ids.id.isin(df_exif.id)]
        print(f'Removed {length_before - len(df_photo_ids)} entries because they are in the exif file already.')

        # Iterate through dataframe, query API for EXIF data and add to another dataframe (and csv!)
        length = len(df_photo_ids)
        print(f'Number of rows of dataframe: {length}')

        # start timer
        start_time = time.time()

        # Count the number of added entries
        counter = 0

        for i, row in df_photo_ids.iterrows():

            # Query the API
            try:
                exif_data = flickr.photos.getExif(photo_id = row['id'], photo_secret = 'secret').get('photo').get('exif')

                # Print counter
                print(f'{datetime.now().strftime("%H:%M:%S")}: Added entry {counter}: {row["id"]}, {row["title"]} | {length - counter} remaining')
                
                # Temporary dict
                dict_tmp = {}

                # Go through every EXIF key value pair available and add to tmp dict
                for exif in exif_data:
                    key = exif.get('label')
                    value = exif.get('raw').get('_content')
                    dict_tmp[key] = value

                # Add ID from ID dataframe
                dict_tmp.update({'id': row['id']})
                dict_tmp.update({'owner': row['owner']})
                dict_tmp.update({'secret': row['secret']})
                dict_tmp.update({'title': row['title']})
                
                # Look for geodata and add it
                try:
                    geodata = flickr.photos.geo.getLocation(photo_id = row['id'])

                    lat = geodata.get('photo').get('location').get('latitude')
                    lon = geodata.get('photo').get('location').get('longitude')
                    acc = geodata.get('photo').get('location').get('accuracy')

                    dict_tmp.update({'lat': lat})
                    dict_tmp.update({'lon': lon})
                    dict_tmp.update({'acc': acc})

                    # Look up reverse geocoding by querying maps API

                    country, admin_lvl1, admin_lvl2, city = '', '', '', ''

                    # Query the API with the location data
                    try:
                        geo = gmaps.reverse_geocode((lat, lon))

                        # Get the data from the response
                        for comp in geo[0].get('address_components'):
                            if 'country' in comp.get('types'):
                                country = comp.get('long_name')
                            if 'administrative_area_level_1' in comp.get('types'):
                                admin_lvl1 = comp.get('long_name')
                            if 'administrative_area_level_2' in comp.get('types'):
                                admin_lvl2 = comp.get('long_name')
                            if 'locality' in comp.get('types'):
                                city = comp.get('long_name')
                            elif 'postal_town' in comp.get('types'):
                                city = comp.get('long_name')

                        dict_tmp.update({'country': country})
                        dict_tmp.update({'admin_lvl1': admin_lvl1})
                        dict_tmp.update({'admin_lvl2': admin_lvl2})
                        dict_tmp.update({'city': city})

                        print(f'Added geodata: {lat}, {lon} in {country}, {admin_lvl1}, {admin_lvl2}, {city}')
                        
                    except googlemaps.exceptions.ApiError as err :
                        print('API key is invalid')

                        dict_tmp.update({'country': 'na'})
                        dict_tmp.update({'admin_lvl1': 'na'})
                        dict_tmp.update({'admin_lvl2': 'na'})
                        dict_tmp.update({'city': 'na'})


                except flickrapi.exceptions.FlickrError as ex:

                    # Add n/a if there's no geodata
                    dict_tmp.update({'lat': 'na'})
                    dict_tmp.update({'lon': 'na'})
                    dict_tmp.update({'acc': 'na'})
                    dict_tmp.update({'country': 'na'})
                    dict_tmp.update({'admin_lvl1': 'na'})
                    dict_tmp.update({'admin_lvl2': 'na'})
                    dict_tmp.update({'city': 'na'})

                    print(f'!!! Geo: Error code: {ex.code} for id {row["id"]}')

                # Add to dataframe
                df_photo_exif.loc[len(df_photo_exif)] = dict_tmp

                # Filename of csv to add data to
                filename = './data/df_photo_exif_final.csv'
                #filename = './data/df_photo_exif_final_bak.csv'
                
                # Create a temporary dataframe
                df_tmp = pd.DataFrame(columns = columns_df_photo_exif)
                df_tmp.loc[len(df_tmp)] = dict_tmp

                # If there is not enough information in dataset, do not add to csv
                #if len(df_tmp[df_tmp.count(axis='columns') >= 5]) > 0:
                df_tmp.to_csv(filename, mode='a', header=not os.path.exists(filename))
                #else:
                #    print('Not enough data, sry.')

            except flickrapi.exceptions.FlickrError as ex:
                print(f'!!! Error code: {ex.code} for id {row["id"]}')
            
            # Delete row from photo id dataframe
            df_photo_ids = df_photo_ids.drop(i)

            counter += 1

        # end the timer and calculate duration
        end_time = time.time()
        minutes, seconds = divmod(int(end_time - start_time), 60)
        per_hour = counter / (end_time - start_time) * 3600

        print(f'Fetched {counter} entries in {minutes} minutes and {seconds} seconds ({per_hour} per hour).')

    except Exception:
            traceback.print_exc()