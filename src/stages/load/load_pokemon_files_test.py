# pylint: disable=W0621
import os
from unittest.mock import patch
import pandas as pd
import matplotlib.pyplot as plt
import pytest
from src.errors.load_error import LoadError
from src.stages.load.load_pokemon_files import LoadPokemonFiles
from src.stages.contracts.transform_contract import TransformContract


@pytest.fixture
def mock_transform_contract():
    """
    Mock TransformContract
    """
    return TransformContract(
        transformation_content={
            "graphic_information": plt.figure(),
            "top_5_higher_exp_base": pd.DataFrame(
                {
                    "Id": [1, 2, 3, 4, 5],
                    "Nome": ["Pikachu", "Charizard", "Bulbasaur", "Squirtle", "Eevee"],
                    "Experiencia_Base": [112, 240, 64, 63, 65],
                    "Tipos": [
                        ["Electric"],
                        ["Fire", "Flying"],
                        ["Grass"],
                        ["Water"],
                        ["Normal"],
                    ],
                }
            ),
            "mean_statistics_by_type": pd.DataFrame(
                {
                    "HP": [35, 78, 45, 44, 55],
                    "Ataque": [55, 84, 49, 48, 55],
                    "Defesa": [40, 78, 49, 65, 50],
                }
            ),
        },
        transformation_date=pd.Timestamp.now(),
    )


def test_load_pokemon_files_success(mock_transform_contract):
    """
    testing function
    """

    loader = LoadPokemonFiles()

    with patch.object(
        LoadPokemonFiles, "load_graphic_bar_by_type"
    ) as mock_graphic, patch.object(LoadPokemonFiles, "generate_report") as mock_report:
        loader.load(mock_transform_contract)

        # confirm if the methods was called if right args just once
        mock_graphic.assert_called_once_with(
            mock_transform_contract.transformation_content["graphic_information"]
        )
        mock_report.assert_called_once_with(
            mock_transform_contract.transformation_content["top_5_higher_exp_base"],
            mock_transform_contract.transformation_content["mean_statistics_by_type"],
        )


def test_load_pokemon_files_error(mock_transform_contract):
    """
    testing error
    """

    loader = LoadPokemonFiles()

    # confirms if the error is currect
    with patch.object(
        LoadPokemonFiles,
        "load_graphic_bar_by_type",
        side_effect=Exception("Simulated error"),
    ):
        with pytest.raises(LoadError) as excinfo:
            loader.load(mock_transform_contract)

        assert "Simulated error" in str(excinfo.value)


def test_load_graphic_bar_by_type():
    """
    testing function
    """

    loader = LoadPokemonFiles()
    graphic = plt.figure()

    with patch("os.makedirs") as mock_makedirs, patch.object(
        graphic, "savefig"
    ) as mock_savefig:
        loader.load_graphic_bar_by_type(graphic)

        # confirm if the methods was called if right args just once
        mock_makedirs.assert_called_once_with(
            os.path.join(os.getcwd(), "outputs"), exist_ok=True
        )
        mock_savefig.assert_called_once_with(
            os.path.join(os.getcwd(), "outputs", "pokemon_tipo_distribuicao.png"),
            format="png",
            dpi=300,
        )
        plt.close(graphic)


def test_generate_report(mock_transform_contract):
    """
    testing function
    """

    loader = LoadPokemonFiles()

    top_5_exp_base = mock_transform_contract.transformation_content[
        "top_5_higher_exp_base"
    ]
    mean_of_statistic = mock_transform_contract.transformation_content[
        "mean_statistics_by_type"
    ]

    with patch("os.makedirs") as mock_makedirs, patch(
        "pandas.DataFrame.to_csv"
    ) as mock_to_csv:
        loader.generate_report(top_5_exp_base, mean_of_statistic)

        # confirm if the methods was called if right args just once
        mock_makedirs.assert_called_once_with(
            os.path.join(os.getcwd(), "outputs"), exist_ok=True
        )
        mock_to_csv.assert_called_once()
