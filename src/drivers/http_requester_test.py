import unittest
from unittest.mock import patch
from .http_requester import HttpRequester
from .mocks.http_requester_mock import (
    mock_get_100_pokemons_from_api,
    mock_get_unique_pokemon_data,
)


class TestHttpRequester(unittest.TestCase):
    """
    testing the get_100_pokemons_from_ap from http_requeter.py
    and testing the get_unique_pokemon_data from http_requeter.py
    """

    @patch("requests.get")
    def test_get_100_pokemons_from_api(self, mock_get):
        """
        testing the get_100_pokemons_from_api
        """

        mock_response = mock_get_100_pokemons_from_api()

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        requester = HttpRequester()

        result = requester.get_100_pokemons_from_api()

        assert "status_code" in result
        assert "informations" in result
        assert result["status_code"] == 200
        assert len(result["informations"]["results"]) == 2
        assert result["informations"]["results"][0]["name"] == "bulbasaur"

    @patch("requests.get")
    def test_get_unique_pokemon_data(self, mock_get):
        """
        testing the get_unique_pokemon_data
        """

        mock_response = mock_get_unique_pokemon_data()

        http_request = HttpRequester()

        mock_get.return_value.json.return_value = mock_response

        url = "https://pokeapi.co/api/v2/pokemon/1/"

        get_dictionary = http_request.get_unique_pokemon_data(url=url)

        assert len(get_dictionary.keys()) == 20
        assert get_dictionary["name"] == "bulbasaur"
        assert get_dictionary["weight"] == 69
        assert get_dictionary["abilities"][0]["ability"]["name"] == "overgrow"
