# Capstone project 'General Market Research on flickr.com Metadata'

In this project we gathered image metadata from the flickr.com API, enrich this data with other sources and check our hypotheses against.

## Presentation

![Capstone Presentation_ Flickr Metadata](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/1a59ef69-a1cc-497f-9f42-7592c9e54671)
![Capstone Presentation_ Flickr Metadata-2](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/eaec69b3-e286-40fd-a81d-9184e317cac4)
![Capstone Presentation_ Flickr Metadata-3](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/83b18c8e-8fe2-4576-b956-be1471b56016)
![Capstone Presentation_ Flickr Metadata-4](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/8d8bb126-7e0a-44d8-b9ac-17c2908653df)
![Capstone Presentation_ Flickr Metadata-5](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/9f016263-8316-4947-9a73-2df6d483f133)
![Capstone Presentation_ Flickr Metadata-6](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/f4b4586f-9ac2-486a-b8e9-347d5de714a6)
![Capstone Presentation_ Flickr Metadata-7](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/0b6cbca2-3bf8-442a-8755-9692a706a497)
![Capstone Presentation_ Flickr Metadata-8](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/666290f8-96ee-48bd-b4f8-ef3f1635727b)
![Capstone Presentation_ Flickr Metadata-9](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/400cf87f-06ce-476d-ab86-441cd1a5bc63)
![Capstone Presentation_ Flickr Metadata-10](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/35c9ed09-39f3-44c7-8885-8a9921b99101)
![Capstone Presentation_ Flickr Metadata-11](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/a24d3300-8607-4721-8928-4793693779c2)
![Capstone Presentation_ Flickr Metadata-12](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/bdf59855-90f9-4ff1-b76f-c9ab3bebdcd4)
![Capstone Presentation_ Flickr Metadata-13](https://github.com/BrittaZa/Capstone_Flickr_Metadata/assets/3992727/f761405b-49ee-4d09-b563-db7beaef9929)


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
