from typing import Dict
import requests
from .interfaces.http_request import HttpRequesterInterface


class HttpRequester(HttpRequesterInterface):
    """
    Class to getting dada from pokemon API
    """

    def __init__(self) -> None:
        self.__url = "https://pokeapi.co/api/v2/pokemon?limit=100&offset=0"

    def get_100_pokemons_from_api(self) -> Dict[int, Dict]:
        """
        Consume informations by url
        -params - url hard code
        -return - dictionary with status code and informations colected from API
        """

        response = requests.get(self.__url, timeout=10)

        if response.status_code == 200:
            return {
                "status_code": response.status_code,
                "informations": response.json(),
            }

        return {
            "status_code": response.status_code,
            "informations": {
                "details": response.text,
            },
        }

    def get_unique_pokemon_data(self, url: str) -> Dict[str, dict]:
        """
        collecte some information from a single pokemon in url
        - params: url: url from a unique pokemon
        - return: a dictonary with all informations about that pokemon
        """

        response = requests.get(url, timeout=10)

        data = response.json()

        return data
