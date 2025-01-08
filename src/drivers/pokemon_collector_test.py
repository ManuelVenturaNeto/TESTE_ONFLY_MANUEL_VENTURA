# pylint: disable= W0108, E1111, C0411, R0801, W0012
import pytest
import unittest
from unittest.mock import patch
from .mocks.pokemon_collector_mock import (
    mock_get_100_pokemons_from_api,
    mock_test_get_unique_pokemon_data,
)
from .pokemon_collector import PokemonCollector, HttpRequester


@pytest.mark.skip(reason="Ignorando todo o arquivo")
class TestPokemonCollector(unittest.TestCase):
    """
    testing the collect_essential_informations from pokemon_collector.py
    """

    @patch.object(
        HttpRequester,
        "get_100_pokemons_from_api",
        side_effect=mock_get_100_pokemons_from_api(),
    )
    @patch.object(
        HttpRequester,
        "get_unique_pokemon_data",
        side_effect=lambda url: mock_test_get_unique_pokemon_data(url),
    )
    def test_collect_essential_informations(self, mock_get_unique, mock_get_100):
        """
        Testing collect_essential_informations
        """

        collector = PokemonCollector()

        result = collector.collect_essential_informations()

        expected_result = {
            "1": {
                "name": "bulbasaur",
                "base_experience": 64,
                "types": ["grass", "poison"],
                "hp": 45,
                "attack": 49,
                "defense": 49,
            },
            "2": {
                "name": "ivysaur",
                "base_experience": 142,
                "types": ["grass", "poison"],
                "hp": 60,
                "attack": 62,
                "defense": 63,
            },
        }

        self.assertEqual(result, expected_result)

        mock_get_100.assert_called_once()
        mock_get_unique.assert_called()

        mock_get_unique.assert_any_call("https://pokeapi.co/api/v2/pokemon/1/")
        mock_get_unique.assert_any_call("https://pokeapi.co/api/v2/pokemon/2/")
