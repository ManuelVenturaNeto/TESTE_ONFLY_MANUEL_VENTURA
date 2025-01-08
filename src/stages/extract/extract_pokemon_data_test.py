from datetime import datetime
import pytest
from src.stages.extract.extract_pokemon_data import ExtractPokemonData
from src.errors.extract_error import ExtractError
from src.stages.extract.mocks.pokemon_collector_mock import (
    mock_collect_essential_informations,
)


def test_collect_essential_informations():
    """
    Testing collect_essential_informations
    """

    collector = ExtractPokemonData()

    result = collector.collect_essential_informations()

    assert isinstance(result.raw_information_content, dict)
    assert isinstance(result.extraction_date, datetime)
    assert result.raw_information_content == mock_collect_essential_informations()
    assert abs((result.extraction_date - datetime.now()).total_seconds()) < 60


def test_collect_essential_informations_error(mocker):
    """
    Testing error of collect_essential_informations
    """

    collector = ExtractPokemonData()

    # forcing error with a mock exception
    mocker.patch.object(
        collector.http_requester,
        "get_100_pokemons_from_api",
        side_effect=Exception("Simulated error"),
    )

    with pytest.raises(ExtractError) as excinfo:
        collector.collect_essential_informations()

    assert "Simulated error" in str(excinfo.value)
    assert excinfo.value.error_type == "Extract Error"
