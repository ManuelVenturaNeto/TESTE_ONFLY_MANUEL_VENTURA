import logging
from typing import Dict
import requests
from src.errors.driver_error import DriverError
from .interfaces.http_request import HttpRequesterInterface


class HttpRequester(HttpRequesterInterface):
    """
    Class to getting dada from pokemon API
    """

    def __init__(self) -> None:
        self.__url = "https://pokeapi.co/api/v2/pokemon?limit=100&offset=0"

        self.log = logging.getLogger(__name__)
        self.log.debug("HttpRequester Started")

    def get_100_pokemons_from_api(self) -> Dict[int, Dict]:
        """
        Consume informations by url
        -params - url hard code
        -return - dictionary with status code and informations colected from API
        """

        try:
            response = requests.get(self.__url, timeout=10)
            self.log.debug("Success to connect with Poke API")
        except:
            self.log.error("Fail to connect with Poke API")

        # if the function connect with API ir continue
        try:
            self.log.debug("Success to connect with Poke API")
            return {
                "status_code": response.status_code,
                "informations": response.json(),
            }
        # if the function cannot connect with API raise an error
        except Exception as exception:  # pylint: disable=broad-except
            self.log.error("Error to make a request with Poke API")
            raise DriverError(str(exception)) from exception

    def get_unique_pokemon_data(self, url: str) -> Dict[str, dict]:
        """
        collecte some information from a single pokemon in url
        - params: url: url from a unique pokemon
        - return: a dictonary with all informations about that pokemon
        """

        # if the function connect with API ir continue
        try:
            try:
                response = requests.get(url, timeout=10)
                self.log.debug("Success to connect with Poke API")
            except:
                self.log.error("Fail to connect with Poke API")

            data = response.json()

            return data

        # if the function cannot connect with API raise an error
        except Exception as exception:  # pylint: disable=broad-except
            self.log.error("Error to make a request with Poke API")
            raise DriverError(str(exception)) from exception
