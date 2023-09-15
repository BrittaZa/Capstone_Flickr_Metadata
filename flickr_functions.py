# Function for removing dupes from dataframe
def df_remove_dupes(df):
    len_before = len(df)
    df = df.drop_duplicates(ignore_index=False)
    len_after = len(df)
    print(f'Found {len_before - len_after} duplicates. Dataframe is now {len(df)} rows long.')
    return df