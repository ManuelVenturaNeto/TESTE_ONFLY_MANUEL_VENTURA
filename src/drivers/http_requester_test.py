# pylint: disable=W0621

import logging
from unittest.mock import patch, MagicMock
import pytest
from src.drivers.http_requester import HttpRequester
from src.errors.driver_error import DriverError


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture
def mock_http_requester():
    """
    Fixture to instantiate the HttpRequester class
    """
    return HttpRequester()


@patch("requests.get")
def test_get_100_pokemons_from_api_success(mock_get, mock_http_requester):
    """
    Test successful response from get_100_pokemons_from_api
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [
            {"name": "Pikachu", "url": "https://pokeapi.co/api/v2/pokemon/25/"},
            {"name": "Charizard", "url": "https://pokeapi.co/api/v2/pokemon/6/"},
        ]
    }
    mock_get.return_value = mock_response

    result = mock_http_requester.get_100_pokemons_from_api()

    assert result["status_code"] == 200
    assert "informations" in result
    assert len(result["informations"]["results"]) == 2
    assert result["informations"]["results"][0]["name"] == "Pikachu"

    logger.debug("Test 'test_get_100_pokemons_from_api_success' passed successfully")


@patch("requests.get")
def test_get_100_pokemons_from_api_failure(mock_get, mock_http_requester):
    """
    Test failed response from get_100_pokemons_from_api
    """
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.side_effect = Exception("Not Found")
    mock_get.return_value = mock_response

    # Here we are asserting that the exception is raised
    with pytest.raises(DriverError, match="Not Found"):
        mock_http_requester.get_100_pokemons_from_api()

    logger.debug("Test 'test_get_100_pokemons_from_api_failure' passed successfully")


@patch("requests.get")
def test_get_unique_pokemon_data_success(mock_get, mock_http_requester):
    """
    Test successful response from get_unique_pokemon_data
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "name": "Pikachu",
        "base_experience": 112,
        "types": [{"type": {"name": "Electric"}}],
        "stats": [
            {"stat": {"name": "hp"}, "base_stat": 35},
            {"stat": {"name": "attack"}, "base_stat": 55},
            {"stat": {"name": "defense"}, "base_stat": 40},
        ],
    }
    mock_get.return_value = mock_response

    url = "https://pokeapi.co/api/v2/pokemon/25/"
    result = mock_http_requester.get_unique_pokemon_data(url)

    assert result["name"] == "Pikachu"
    assert result["base_experience"] == 112
    assert result["types"][0]["type"]["name"] == "Electric"
    assert result["stats"][0]["stat"]["name"] == "hp"
    assert result["stats"][0]["base_stat"] == 35

    logger.debug("Test 'test_get_unique_pokemon_data_success' passed successfully")


@patch("requests.get")
def test_get_unique_pokemon_data_failure(mock_get, mock_http_requester):
    """
    Test failed response from get_unique_pokemon_data
    """
    mock_response = MagicMock()
    mock_response.json.side_effect = Exception("Simulated error")
    mock_get.return_value = mock_response

    url = "https://pokeapi.co/api/v2/pokemon/99999/"
    with pytest.raises(DriverError, match="Simulated error"):
        mock_http_requester.get_unique_pokemon_data(url)

    logger.debug("Test 'test_get_unique_pokemon_data_failure' passed successfully")
