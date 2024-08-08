import base64
import re

import cloudscraper
from urllib.parse import quote

import urllib.parse
from bs4 import BeautifulSoup
from urllib.parse import unquote
from typing import Optional, Dict, List

from utils import VidSrcError, general_dec, general_enc
from Video_Extractors.f2cloud import F2Cloud

def get_vidplay_subtitles(url_data: str) -> Dict:
        scraper = cloudscraper.create_scraper()
        subtitles_url = re.search(r"info=([^&]+)", url_data)
        if not subtitles_url:
            return []

        subtitles_url_formatted = unquote(subtitles_url.group(1))
        req = scraper.get(subtitles_url_formatted)

        if req.status_code == 200:
            json_output = [
                {"label": subtitle.get("label"), "file": subtitle.get("file")}
                for subtitle in req.json()
            ]
            return json_output

        return []

class WatchSeriesExtractor:
    BASE_URL = "watchseriesx.to"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
    scraper = cloudscraper.create_scraper()

    @staticmethod
    def dec(inp):
        return general_dec('8z5Ag5wgagfsOuhz', inp)

    @staticmethod
    def enc(inp):
        return general_enc('Ex3tc7qjUz7YlWpQ', inp)

    @staticmethod
    def extract_info(array: List) -> List:
        json_array = []
        for media in array:
            # Used to get title and media_id
            info = media.find('div',class_="info")
            media_id = info.find('a',class_="title")['href']
            title = info.find('a',class_="title").text.strip()

            # Inner contains quality and image_uri
            inner = media.find('div',class_="inner")
            quality = inner.find('b').text.strip()
            image_uri = inner.find('a',class_="poster").find('img')['data-src']

             # Create a dictionary for the current match
            json_object = {
                "title": title,
                "image_uri": image_uri,
                "quality": quality,
                "show_type": media_id.split('/')[1],
                "media_id": media_id
            }

            # Append the dictionary to the JSON array
            json_array.append(json_object)

        return json_array

    def fetch_trending_info(self,result_set) -> List:
        return self.extract_info(result_set.find('div',class_="swiper-wrapper item-lg").find_all('div',class_="swiper-slide item"))

    def return_trending_json(self) -> Dict:
        url = f"https://{self.BASE_URL}/home"
        req = self.scraper.get(url)

        if req.status_code != 200:
            print(f"FAILED {url} {req.status_code}")

        soup = BeautifulSoup(req.content,"html.parser")
        trending_media = soup.find_all('section',class_ = "swiper-default") # Gets info for trending tv and movies
        trending_overrall = soup.find('div',attrs={"data-name":"trending"}).find_all('div',class_='item')

        if len(trending_media) <= 0:
            return {
                "top_trending_media": [],
                "trending_movies": [],
                "trending_tv": []
             }

        return {
            "top_trending_media": self.extract_info(trending_overrall),
            "trending_movies": self.fetch_trending_info(trending_media[0]),
            "trending_tv": self.fetch_trending_info(trending_media[1])
        }

    def fetch_search_results(self,query: str) -> Dict:
        url = f"https://{self.BASE_URL}/filter?keyword={query}"
        req = self.scraper.get(url)

        if req.status_code != 200:
            raise VidSrcError(f"Couldnt fetch {req.url}, status code: {req.status_code}...")

        soup = BeautifulSoup(req.content,"html.parser")
        results = soup.find('div',class_="item-lg")
        if not results:
            print("Results Not Found")
            return {
                "total_pages": 0,
                "results": []
            }

        results = self.extract_info(results.find_all('div',class_="item"))
        return {
            "total_pages": 0,
            "results": results
        }

    def fetch_season_episode_list(self,data_id: str) -> Dict:
        # Get Episode List
        season_episodes = {}

        encoded_data_id = self.enc(data_id)
        url = f"https://{self.BASE_URL}/ajax/episode/list/{data_id}?vrf={urllib.parse.unquote(encoded_data_id)}"
        req = self.scraper.get(url)

        if req.status_code != 200:
            raise VidSrcError(f"Couldnt fetch {req.url}, status code: {req.status_code}...")
        soup = BeautifulSoup(req.json().get('result'),'html.parser')

        seasons = soup.find_all('ul',class_="range episodes")
        for season in seasons:
            season_num = season['data-season']
            episode_array = []
            for episode in season.find_all('li'):
                episode_array.append({
                    "name":episode.find('a').find('span').text.strip(),
                    "id": episode.find('a')['data-id'],
                    "url":episode.find('a')['href'],
                    "episode_num":episode.find('a').find('p').text.strip().replace("Episode ","")
                })
            season_episodes[season_num] = episode_array

        return season_episodes

    def fetch_media_details(self,media_id: str) -> Dict:
        genres = []
        url = f"https://{self.BASE_URL}{media_id}"
        req = self.scraper.get(url)

        if req.status_code != 200:
            raise VidSrcError(f"Couldnt fetch {req.url}, status code: {req.status_code}...")

        soup = BeautifulSoup(req.content,"html.parser")

        details_info = soup.find('div',class_="col-info")
        title = details_info.find('h3',attrs={"itemprop":"name"}).text.strip()
        score = details_info.find('span',class_="imdb").text.strip()
        rating = details_info.find('span',class_="rating").text.strip()
        quality = details_info.find('span',class_="quality").text.strip()
        description = details_info.find('div',class_="description").text.strip()
        image_uri = details_info.find('img',attrs={"itemprop":"image"})["src"]

        # Get Genres and Release Date
        other_info = details_info.find('div',class_="meta").find_all('div',class_=None)
        release_date = details_info.find('div',class_="meta").find('span',attrs={"itemprop": "dateCreated"}).text.strip().split(', ')[-1]

        for info in other_info:
            category = info.find('div')
            if category and category.text.strip() == "Genre:":
                for genre in info.find_all('a'):
                    genres.append(genre.text.strip())
                break

        recommendations = self.extract_info(soup.find('section',class_="swiper-default").find_all('div',class_="swiper-slide item"))

        data_id = re.search(r'data-id="(.*?)"', req.text).group(1)
        if not data_id:
            print("[VidSrcExtractor] Could not fetch data-id, this could be due to an invalid imdb/tmdb code...")
            return None, None, None

        season_episodes = self.fetch_season_episode_list(data_id)

        return {
            "title": title,
            "id": media_id,
            "banner_image_uri": "",
            "synopsis": description,
            "rating": rating,
            "score": score,
            "release_date": release_date,
            "image_uri": image_uri,
            "country": "",
            "quality": quality,
            "tmdb_id": "",
            "trailer_uri": "",
            "show_type": media_id.split('/')[1],
            "episodes": season_episodes,
            "genres": genres,
            "cast": [],
            "production_company": [],
            "recommendations": recommendations
        }

    def fetch_episode(self,data_id) -> List:
        # print(f"asdasdasd {data_id}")
        url = f"https://{self.BASE_URL}/ajax/server/list/{data_id}?vrf={urllib.parse.unquote(self.enc(data_id))}"
        req = self.scraper.get(url)
        if req.status_code != 200:
            raise VidSrcError(f"Couldnt fetch {req.url}, status code: {req.status_code}...")

        req = req.json()
        f2_cloud_id = re.search(r'data-id="41" data-link-id="(.*?)"', req['result']).group(1)

        url = f"https://{self.BASE_URL}/ajax/server/{f2_cloud_id}?vrf={urllib.parse.quote(self.enc(f2_cloud_id))}"

        req = self.scraper.get(url)

        if req.status_code != 200:
            print(f"FAILED {url} {req.status_code}")

        f2cloud_url_dec = self.dec(req.json()['result']['url'])
        return F2Cloud().stream(f2cloud_url_dec)

    def get_streams(self, media_id: str, season: Optional[str], episode: Optional[str]):
        url = f"https://{self.BASE_URL}/tv/{media_id}/{season}-{episode}"

        req = self.scraper.get(url)
        print(f"[>] Requesting {url}...")
        if req.status_code != 200:
            raise VidSrcError(f"Couldnt fetch {req.url}, status code: {req.status_code}...")

        data_id = re.search(r'data-id="(.*?)"', req.text).group(1)

        if not data_id:
            print("[VidSrcExtractor] Could not fetch data-id, this could be due to an invalid imdb/tmdb code...")
            return []

        encoded_data_id = self.enc(data_id)
        url = f"https://{self.BASE_URL}/ajax/episode/list/{data_id}?vrf={urllib.parse.unquote(encoded_data_id)}"

        req = self.scraper.get(url)
        if req.status_code != 200:
            raise VidSrcError(f"Couldnt fetch {req.url}, status code: {req.status_code}...")

        req = req.json()
        data_id = re.search(f'{season}-{episode}" data-id="(.*?)"', req['result']).group(1)
        return self.fetch_episode(data_id)

if __name__ == '__main__':
    vs =  WatchSeriesExtractor()
    vs.fetch_media_details("/tv/naked-and-afraid-last-one-standing-q6kpw")