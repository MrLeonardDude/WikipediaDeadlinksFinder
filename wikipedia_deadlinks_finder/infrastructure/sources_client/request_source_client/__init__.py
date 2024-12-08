from aiohttp import ClientSession
from requests.exceptions import ConnectionError, ReadTimeout
from os import environ

from wikipedia_deadlinks_finder.domains.wikipedia_source import WikipediaSource
from wikipedia_deadlinks_finder.utils.logger import logger


class RequestSourceClient:

    def __init__(self):
        self.session = ClientSession()

    async def validate_source(self, wikipedia_source: WikipediaSource) -> bool:
        try:
            response = await self.session.get(
                wikipedia_source.url,
                allow_redirects=False,
                timeout=int(environ.get("TIMEOUT_IN_SECONDS", "3")),
            )
        except Exception as e:
            logger.warn("problem connecting...")
            return False

        if response.status == 404 or response.status == 500:
            logger.warn("found deadlink...")
            return False

        return True
    
    async def close(self):
        await self.session.close()
