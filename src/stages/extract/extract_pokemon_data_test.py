# pylint: disable=W0621

import logging
from unittest.mock import MagicMock
import pytest
from src.stages.extract.extract_pokemon_data import ExtractPokemonData
from src.errors.extract_error import ExtractError
from src.stages.contracts.extract_contract import ExtractContract

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture
def mock_extractor():
    """
    Fixture para instanciar a classe ExtractPokemonData.
    """
    return ExtractPokemonData()


def test_collect_essential_informations_success(mock_extractor):
    """
    Testa a execução bem-sucedida de `collect_essential_informations`.
    """
    # Mockando o método get_100_pokemons_from_api
    mock_extractor.http_requester.get_100_pokemons_from_api = MagicMock(
        return_value={
            "informations": {
                "results": [
                    {"name": "Pikachu", "url": "https://pokeapi.co/api/v2/pokemon/25/"},
                    {
                        "name": "Charizard",
                        "url": "https://pokeapi.co/api/v2/pokemon/6/",
                    },
                ]
            }
        }
    )

    # Mockando o método get_unique_pokemon_data
    mock_extractor.http_requester.get_unique_pokemon_data = MagicMock(
        side_effect=[
            {
                "base_experience": 112,
                "types": [{"type": {"name": "Electric"}}],
                "stats": [
                    {"stat": {"name": "hp"}, "base_stat": 35},
                    {"stat": {"name": "attack"}, "base_stat": 55},
                    {"stat": {"name": "defense"}, "base_stat": 40},
                ],
            },
            {
                "base_experience": 240,
                "types": [{"type": {"name": "Fire"}}, {"type": {"name": "Flying"}}],
                "stats": [
                    {"stat": {"name": "hp"}, "base_stat": 78},
                    {"stat": {"name": "attack"}, "base_stat": 84},
                    {"stat": {"name": "defense"}, "base_stat": 78},
                ],
            },
        ]
    )

    result = mock_extractor.collect_essential_informations()

    # check the tipe of data is currect
    assert isinstance(result, ExtractContract)

    # check if the the result have the expect mock data vales
    assert "25" in result.raw_information_content
    assert "6" in result.raw_information_content

    # check if the method call the exprected params to a mock element
    pikachu = result.raw_information_content["25"]
    assert pikachu["Nome"] == "Pikachu"
    assert pikachu["Experiencia_Base"] == 112
    assert pikachu["Tipos"] == ["Electric"]
    assert pikachu["HP"] == 35
    assert pikachu["Ataque"] == 55
    assert pikachu["Defesa"] == 40

    charizard = result.raw_information_content["6"]
    assert charizard["Nome"] == "Charizard"
    assert charizard["Experiencia_Base"] == 240
    assert charizard["Tipos"] == ["Fire", "Flying"]
    assert charizard["HP"] == 78
    assert charizard["Ataque"] == 84
    assert charizard["Defesa"] == 78

    logger.debug(
        "Test 'test_collect_essential_informations_success' passed successfully"
    )


def test_collect_essential_informations_error(mock_extractor):
    """
    testing error
    """

    # mocking an error in the function
    mock_extractor.http_requester.get_100_pokemons_from_api = MagicMock(
        side_effect=Exception("Simulated API error")
    )

    # testing if the error raises
    with pytest.raises(ExtractError) as excinfo:
        mock_extractor.collect_essential_informations()

    assert "Simulated API error" in str(excinfo.value)

    logger.debug("Test 'ExtractError' passed successfully")
