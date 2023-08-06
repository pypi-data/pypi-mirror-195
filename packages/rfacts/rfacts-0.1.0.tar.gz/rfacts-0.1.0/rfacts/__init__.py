import requests
import aiohttp

url = "https://uselessfacts.jsph.pl/random.json?language="

class InvalidLangauge(Exception):
    pass

class fact():
    def __init__(self, id: str, source: str, permalink: str, text: str, language: str, raw: dict) -> None:
        self.id: str = id
        self.source: str = source
        self.permalink: str = permalink
        self.text: str = text
        self.language: str = language
        self._raw: dict = raw

    @classmethod
    def get(cls, language: str="en") -> "fact":
        if language not in ("en", "de"): 
            raise InvalidLangauge(f"'{language}' is not a valid language, valid languages are 'en' and 'de'")
        data = requests.get(url+language).json()
        return cls(data['id'], data['source'], data['permalink'], data['text'], language, data)

    @classmethod
    async def aget(cls, language: str="en") -> "fact":
        if language not in ("en", "de"): 
            raise InvalidLangauge(f"'{language}' is not a valid language, valid languages are 'en' and 'de'")
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url+language) as resp:
                data = await resp.json()
        return cls(data['id'], data['source'], data['permalink'], data['text'], language, data)