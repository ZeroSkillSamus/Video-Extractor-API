import requests
import re
import json
import cloudscraper

from urllib.parse import urlparse, quote
from utils import VidSrcError, general_dec, general_enc

class F2Cloud:
    @staticmethod
    def h_enc(inp):
        return general_enc('BgKVSrzpH2Enosgm',inp)

    @staticmethod
    def embed_enc(inp):
        return general_enc('8Qy3mlM2kod80XIK', inp)

    @staticmethod
    def embed_dec(inp):
        return general_dec('9jXDYBZUcTcTZveM', inp)

    def stream(self,url):
        scraper = cloudscraper.create_scraper()
        url = urlparse(url)
        embed_id = url.path.split('/')[2]

        h = self.h_enc(embed_id)

        mediainfo_url = f"https://{url.hostname}/mediainfo/{self.embed_enc(embed_id)}?{url.query}&ads=0&h={quote(h)}"
        print(f"New URL {mediainfo_url}")
        req = scraper.get(mediainfo_url)

        if req.status_code != 200:
            print(f"Failed! {mediainfo_url}    {req.status_code}")

        req = req.json()
        playlist = json.loads(self.embed_dec(req['result']))
        sources = playlist.get('sources')
        json_array = []

        # Need to request the m3u8 file to get other qualities
        sources = [value.get("file") for value in sources]
        req = requests.get(sources[0])
        if req.status_code != 200:
            error_msg = f"Couldnt fetch {req.url}, status code: {req.status_code}..."
            raise VidSrcError(error_msg)

        pattern = re.compile(r"(RESOLUTION=)(.*)(\s*?)(\s*.*)")
        index_to_start = sources[0].index("list;")
        for match in pattern.finditer(req.text):
            quality = match.group(2).split("x")[-1]
            url = sources[0][:index_to_start] + match.group(4).strip()

            # Create a dictionary for the current match
            json_object = {
                "quality": quality,
                "url": url,
                "is_m3u8": ".m3u8" in url
            }

            # Append the dictionary to the JSON array
            json_array.append(json_object)

        return json_array