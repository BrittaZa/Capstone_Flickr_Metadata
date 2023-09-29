
# Capstone Project on flickr metadata

## - copied nf_sql env as nf_sql_cap and added flickrapi package

## downloaded unique user information from flickr people.get info 
- got unique user_id's from our base dataframe
- stored them to a list
- wrote a for loop to only get our userdata

### blocker 
- api breaks from time to time and causes Error
- adds unnamed columns 
- overwrote df and csv by accident
- data was not added to csv bc of the error, fixed it manually

### result: 38.801 rows, 38 columns

## data cleaning first round
- drop unnecessary columns (24), keep (14) 
- lower, replace
- check NAN
- drop rows with NaN in location,...
- boolean for is pro
- check time and dtypes
### blocker 
- inplace true?
## to Do
- get a updated list of unique users where list is not in old list
- write a update loop with sleep and if response== '200' to get rid of Errors
- get locationdata from googleMaps API
- write a cleaning function
- add to user_df
- send dataframe to SQL Database

- clean notebooks

## update uniue owner/user_id
- get a list with unique user_id from df_foto_exif_final
- compare to list user_in_df 
- create a new update list with user not in user_data_cleaned