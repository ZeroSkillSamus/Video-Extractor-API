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
2. `/WATCHSERIES/Search?query=Naruto`
   - Needs 1 query param:
     - query: string to search on watchseries 
   - Example Output:
     ```json
        "results": [
           {
               "image_uri": "https://static.watchseriesx.to/8c/i/6/67/67393aae900cbeab0f4a2cda7cfabcfb@280.jpg",
               "media_id": "/tv/naruto-1e3rj",
               "quality": "HD",
               "show_type": "tv",
               "title": "Naruto"
           }
        ],
        "total_pages": 0
    ```
    
4. `/VIDSRC-TO/Watch?id=tales-of-the-teenage-mutant-ninja-turtles-yk28e&season=1&episode=1`
   - Needs 3 query params:
     - media_id: Represents the `media_id` from watchseries but only the 2nd url argument EX: `tales-of-the-teenage-mutant-ninja-turtles-yk28e`
     - season: Specifies the season number
       - If movie type please specify 1 (will change later to make season and episode optional)
    - episode: Specifies the episode number
       - If movie type please specify 1 (will change later to make season and episode optional)
   - Subtitles will be added later but not a priority since vidsrc subtitles aren't the best
   - Example Output:
      - ```json
         "m3u8_links": [
          {
            "is_m3u8": true,
            "quality": "",
            "url": ""
          }
         ]
        "subtitles": []
        ```
     

   
