import typing
import aiohttp
import logging
from bs4 import BeautifulSoup

from bot.core.config.Config import GeniusConfig
from bot.core.errors.CustomExceptions import APIError

logger = logging.getLogger("apis.genius.genius.GeniusWrapper")


class GeniusWrapper:
    BASE_URI = "https://api.genius.com"
    ANNOTATION_ENDPOINT = "https://api.genius.com/annotations"
    REFERENT_ENDPOINT = "https://api.genius.com/referents"
    SONG_ENDPOINT = "https://api.genius.com/songs"
    ARTIST_ENDPOINT = "https://api.genius.com/artists"
    WEBPAGE_ENDPOINT = "https://api.genius.com/web_pages"
    SEARCH_ENDPOINT = "https://api.genius.com/search"

    def __init__(self):
        self.__session = aiohttp.ClientSession()

        try:
            self.token = GeniusConfig.get_token()
            self.client_id = GeniusConfig.get_client_id()
        except KeyError as k_e:
            logger.exception(str(k_e))
            raise ValueError(f'{"Token" if self.token is None else "Client ID"} not provided in config')

    async def __get(self, url: str, headers: typing.Dict = None, params=None) -> typing.Dict:
        async with self.__session.get(url, params=params, headers=headers) as resp:
            if "application/json" in resp.headers["Content-Type"]:
                data = await resp.json()
            elif "text/html" in resp.headers["Content-Type"]:
                data = await resp.text()

            if resp.status != 200:
                logger.warning(f"Fetching the following URL did not succeed: {url}")
                logger.warning(f"Fetch params {params}, headers {headers}")

            return data

    async def __post(self, url: str, headers: typing.Dict = None, params: typing.Dict = None, body: typing.Dict = None):
        pass

    # NOTE: Maybe beneficial to place this function in the business logic than in the model, and
    # even after repositioning this function, it may need to be split into multiple functions
    def get_lyrics(self, artist: str, song_name: str):
        search_result = None

        if song_name is None or song_name.strip() == "":
            raise ValueError("Song name is empty")

        try:
            search_result = await self.__get(self.SEARCH_ENDPOINT,
                                             params={'q': song_name},
                                             headers={"Authorization": self.token})

            if search_result["meta"]["status"] != 200:
                return None

            song_result = search_result["response"]["hits"][0]["result"]
            song_url = song_result["url"]
            song_art = song_result["song_art_image_url"]

            return self.__lyrics_scraper(song_url)
        except (KeyError, IndexError) as res_obj_err:
            logger.exception(str(res_obj_err))
            logger.info("Search results returned: " + str(search_result))
            raise APIError("An error occurred acquiring search result")
        except aiohttp.InvalidURL as inv_url:
            logger.exception(str(inv_url))
            raise ValueError("URL is invalid")

    def __lyrics_scraper(self, url: str) -> str:
        try:
            page_html_str = await self.__get(url)
            page_html = BeautifulSoup(page_html_str, "html.parser")
            lyrics_str = page_html.find("div", class_="lyrics").get_text()

            return lyrics_str

        except aiohttp.InvalidURL as inv_url:
            raise ValueError("URL provided is invalid")
