import logging
from typing import Dict
import aiohttp # type: ignore
from src.errors.driver_error import DriverError
from .interfaces.http_request import HttpRequesterInterface

class HttpRequester(HttpRequesterInterface):
    """
    Class to getting data from pokemon API
    """

    def __init__(self) -> None:
        self.__url = "https://pokeapi.co/api/v2/pokemon?limit=100&offset=0"
        self.log = logging.getLogger(__name__)
        self.log.debug("HttpRequester Started")

    async def get_100_pokemons_from_api(self) -> Dict[int, Dict]:
        """
        Consume informations by url
        -params - url hard code
        -return - dictionary with status code and informations collected from API
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.__url, timeout=120) as response:
                    self.log.debug("Success to connect with Poke API")
                    return {
                        "status_code": response.status,
                        "informations": await response.json(),
                    }
        except Exception as exception:
            self.log.error("Fail to connect with Poke API")
            raise DriverError(str(exception)) from exception

    async def get_unique_pokemon_data(self, url: str) -> Dict[str, dict]:
        """
        Collect some information from a single pokemon in url
        - params: url: url from a unique pokemon
        - return: a dictionary with all informations about that pokemon
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=120) as response:
                    self.log.debug("Success to connect with Poke API")
                    return await response.json()
        except Exception as exception:
            self.log.error("Error to make a request with Poke API")
            raise DriverError(str(exception)) from exception