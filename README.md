# Video-Extractor-API
Simple Watchseries m3u8 extractor 

## Instructions To Start
1. pip install -r /path/to/requirements.txt
2. python api.py


## Routes
1. `/WATCHSERIES/Trending` 
   - Returns The following JSON
   - ```json
     "top_trending_media": [
     {
        "image_uri": "https://static.watchseriesx.to/8c/i/4/46/460b210a50687d92c4ab4c7986642a9a@280.jpg",
        "media_id": "/tv/house-of-the-dragon-24qye",
        "quality": "HD",
        "show_type": "tv",
        "title": "House of the Dragon"
     },
     {
        "image_uri": "https://static.watchseriesx.to/8c/i/7/7c/18e85b1f14cb53f6db32bd945f7a404d@280.jpg",
        "media_id": "/movie/the-instigators-j4pwn",
        "quality": "HD",
        "show_type": "movie",
        "title": "The Instigators"
     }
     ],
     "trending_movies": [
     {
       "image_uri": "https://static.watchseriesx.to/8c/i/7/7c/18e85b1f14cb53f6db32bd945f7a404d@280.jpg",
       "media_id": "/movie/the-instigators-j4pwn",
       "quality": "HD",
       "show_type": "movie",
       "title": "The Instigators"
     }
     ],
     "trending_tv": [
     {
        "image_uri": "https://static.watchseriesx.to/8c/i/a/a9/de09df466abcf40102c987e4735e03de@280.jpg",
        "media_id": "/tv/tales-of-the-teenage-mutant-ninja-turtles-yk28e",
        "quality": "HD",
        "show_type": "tv",
        "title": "Tales of the Teenage Mutant Ninja Turtles"
     },
     ]
     ```
2. `/WATCHSERIES/Search?query`
3. `/WATCHSERIES/ 
