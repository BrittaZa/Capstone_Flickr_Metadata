### Capstone project 'General Market Research on flickr.com Metadata'

In this project we gathered image metadata from the flickr.com API, enrich this data with other sources and check our hypotheses against.

## Technical links
- [Flickr API reference](https://www.flickr.com/services/api/)<br>
- [Google Maps API](https://developers.google.com/maps/documentation/geocoding/requests-reverse-geocoding?hl=en) for reverse geocoding<br>
- [Random Word API](https://random-word-api.herokuapp.com/home)<br>

## Code snippets
- ```df.notna().sum() * 100 / len(df)``` - Percentage of non null (NaN) values in columns
- ```df1 = df1[~df1.id.isin(df2)]``` - Look if a field (id in this case) is inside of another dataframe
- If you're curious about a actual image you can use the getSizes method to get URLs and download them using wget:
```
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
for index, row in df[df['country'] == 'Greenland'].iterrows():
    sizes = flickr.photos.getSizes(photo_id = row.get('id'))
    for size in sizes.get('sizes').get('size'):
        if size.get('label') == 'Original':
            runcmd('wget ' + size.get('source'), verbose = True)
```
