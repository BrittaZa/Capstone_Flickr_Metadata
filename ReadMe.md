### Capstone project 'Flickr something'

## Project related links
- [Mural](https://app.mural.co/t/capstonegroup17548/m/capstonegroup17548/1695028847653/0130c7107a613d7debad6a107d300824991d3e9e?sender=u05f542ff195922836d850746) for brainstorming<br>
- [Trello](https://trello.com/b/PrN8FCNb) for project management<br>
- [Google Drive](https://drive.google.com/drive/folders/1ZkFgD9vK9iPSk6jFy6anWj8abK70APWi) directory of project related documents

## Technical links
- [Flickr API reference](https://www.flickr.com/services/api/)<br>
- [Google Maps API](https://developers.google.com/maps/documentation/geocoding/requests-reverse-geocoding?hl=en) for reverse geocoding<br>
- [Random Word API](https://random-word-api.herokuapp.com/home)<br>

## Code snippets
- ```df.notna().sum() * 100 / len(df)``` - Percentage of non null (NaN) values in columns
- ```df1 = df1[~df1.id.isin(df2)]``` - Look if a field (id in this case) is inside of another dataframe
- ```flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
for index, row in df[df['country'] == 'Greenland'].iterrows():
    sizes = flickr.photos.getSizes(photo_id = row.get('id'))
    for size in sizes.get('sizes').get('size'):
        if size.get('label') == 'Original':
            runcmd('wget ' + size.get('source'), verbose = True)``` - If you're curious about a actual image you can use the getSizes method to get URLs and download them using wget.

## Johannes' ToDo-List (should be moved somewhere else
- Difference between 'Date and Time (Original)' and 'Date and Time (Digitized)'?
- DONE Add geo data querying to get_metadata
- DONE Reverse geocoding (from lat, lon to region or country). Cannot be done in Tableau. Need to iterate through data and ask an API. Granularity?
- DONE Add reverse geocoding to get_metadata
