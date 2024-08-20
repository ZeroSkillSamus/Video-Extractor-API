import requests
import re
import json
import cloudscraper

from urllib.parse import urlparse, quote
from keys import source_keys
from utils import VidSrcError
from utils import subst_, subst, rc4, reverse, mapp, general_enc

class F2Cloud:
    @staticmethod
    def enc(inp,source):
        keys = source_keys[source]
        a = mapp(inp,keys[0],keys[1])
        a = reverse(a)
        a = rc4(keys[2],a)
        a = subst(a)
        a = reverse(a)
        a = mapp(a,keys[3],keys[4])
        a = rc4(keys[5],a)
        a = subst(a)
        a = rc4(keys[6], a)
        a = subst(a)
        a = reverse(a)
        a = mapp(a, keys[7], keys[8])
        a = subst(a)
        return a

    @staticmethod
    def dec(inp,source):
        keys = source_keys[source]
        a = subst_(inp)
        a = mapp(a, keys[8], keys[7])
        a = reverse(a)
        a = subst_(a)
        a = rc4(keys[6], a)
        a = subst_(a)
        a = rc4(keys[5], a)
        a = mapp(a, keys[4], keys[3])
        a = reverse(a)
        a = subst_(a)
        a = rc4(keys[2], a)
        a = reverse(a)
        a = mapp(a, keys[1], keys[0])
        return a

    def stream(self,url,source):
        scraper = cloudscraper.create_scraper()
        url = urlparse(url)
        embed_id = url.path.split('/')[2]

        mediainfo_url = f"https://{url.hostname}/mediainfo/{self.enc(embed_id,source)}?{url.query}&ads=0"
        req = scraper.get(mediainfo_url)

        if req.status_code != 200:
            print(f"Failed! {mediainfo_url}    {req.status_code}")

        req = req.json()
        playlist = json.loads(self.dec(req['result'],source))
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