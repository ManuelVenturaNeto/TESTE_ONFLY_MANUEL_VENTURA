# pylint: disable=W0621

import logging
from unittest.mock import MagicMock, AsyncMock
import pytest
from src.stages.extract.extract_pokemon_data import ExtractPokemonData
from src.errors.extract_error import ExtractError
from src.stages.contracts.extract_contract import ExtractContract

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture
def mock_extractor():
    """
    Fixture to instantiate the ExtractPokemonData class.
    """
    return ExtractPokemonData()


@pytest.mark.asyncio
async def test_collect_essential_informations_success(mock_extractor):
    """
    Test the successful execution of `collect_essential_informations`.
    """
    # Mocking the get_100_pokemons_from_api method
    mock_extractor.http_requester.get_100_pokemons_from_api = AsyncMock(
        return_value={
            "status_code": 200,
            "informations": {
                "results": [
                    {"name": "Pikachu", "url": "https://pokeapi.co/api/v2/pokemon/25/"},
                    {
                        "name": "Charizard",
                        "url": "https://pokeapi.co/api/v2/pokemon/6/",
                    },
                ]
            },
        }
    )

    # Mocking the get_unique_pokemon_data method
    mock_extractor.http_requester.get_unique_pokemon_data = AsyncMock(
        side_effect=[
            {
                "name": "Pikachu",
                "base_experience": 112,
                "types": [{"type": {"name": "Electric"}}],
                "stats": [
                    {"stat": {"name": "hp"}, "base_stat": 35},
                    {"stat": {"name": "attack"}, "base_stat": 55},
                    {"stat": {"name": "defense"}, "base_stat": 40},
                ],
            },
            {
                "name": "Charizard",
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

    result = await mock_extractor.collect_essential_informations()

    # Check the type of data is correct
    assert isinstance(result, ExtractContract)

    # Check if the result has the expected mock data values
    assert "25" in result.raw_information_content
    assert "6" in result.raw_information_content

    # Check if the method called the expected params for a mock element
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


@pytest.mark.asyncio
async def test_collect_essential_informations_error(mock_extractor):
    """
    Test error handling in `collect_essential_informations`.
    """
    # Mocking an error in the function
    mock_extractor.http_requester.get_100_pokemons_from_api = AsyncMock(
        side_effect=Exception("Simulated API error")
    )

    # Testing if the error is raised
    with pytest.raises(ExtractError) as excinfo:
        await mock_extractor.collect_essential_informations()

    assert "Simulated API error" in str(excinfo.value)

    logger.debug("Test 'ExtractError' passed successfully")