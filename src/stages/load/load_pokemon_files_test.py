# pylint: disable=C0303, W0613

import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd
import matplotlib.pyplot as plt
from src.errors.load_error import LoadError
from src.stages.contracts.transform_contract import TransformContract
from src.stages.load.load_pokemon_files import LoadPokemonFiles


class TestLoadPokemonFiles(unittest.TestCase):
    """
    Testing all function of LoadPokemonFiles
    """

    def setUp(self):
        self.loader = LoadPokemonFiles()
        self.mock_transform_contract = MagicMock(spec=TransformContract)

    @patch.object(os, "makedirs")
    @patch.object(plt.Figure, "savefig")
    def test_load_graphic_bar_by_type(self, mock_savefig, mock_makedirs):
        """
        testing function
        """

        graphic = MagicMock(spec=plt.Figure)

        self.loader.load_graphic_bar_by_type(graphic)

        # Verifica se o diretório foi criado
        mock_makedirs.assert_called_once_with(
            os.path.join(os.getcwd(), "outputs"), exist_ok=True
        )

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("os.makedirs")
    def test_generate_report_csv(self, mock_makedirs, mock_open):
        """
        testing function
        """

        top_5_exp_base = pd.DataFrame(
            {
                "Id": [1, 2, 3, 4, 5],
                "Nome": [
                    "Bulbasaur",
                    "Ivysaur",
                    "Venusaur",
                    "Charmander",
                    "Charmeleon",
                ],
                "Experiencia_Base": [64, 142, 236, 62, 142],
                "Tipos": ["Grama", "Grama", "Grama", "Fogo", "Fogo"],
            }
        )

        mean_of_statistic = pd.DataFrame(
            {
                "Tipo": ["Grama", "Fogo"],
                "HP_Medio": [45.0, 39.0],
                "Ataque_Medio": [49.0, 52.0],
                "Defesa_Media": [49.0, 43.0],
            }
        )

        graphic_path = os.path.join(os.getcwd(), "outputs", "test_graphic.png")

        self.loader.generate_report_csv(top_5_exp_base, mean_of_statistic, graphic_path)

        mock_makedirs.assert_called_once_with(
            os.path.join(os.getcwd(), "outputs"), exist_ok=True
        )
        mock_open.assert_called_once()

    @patch.object(
        LoadPokemonFiles, "load_graphic_bar_by_type", return_value="mock_path.png"
    )
    @patch.object(LoadPokemonFiles, "generate_report_csv")
    def test_load_requered_files(self, mock_generate_report_csv, mock_load_graphic):
        """
        testing function
        """

        self.mock_transform_contract.transformation_content = {
            "graphic_information": MagicMock(spec=plt.Figure),
            "top_5_higher_exp_base": pd.DataFrame(),
            "mean_statistics_by_type": pd.DataFrame(),
        }

        self.loader.load_requered_files(self.mock_transform_contract)

        mock_load_graphic.assert_called_once_with(
            self.mock_transform_contract.transformation_content["graphic_information"]
        )
        mock_generate_report_csv.assert_called_once()

    @patch.object(LoadPokemonFiles, "load_graphic_bar_by_type")
    @patch.object(LoadPokemonFiles, "generate_report_csv")
    def test_load_requered_files_raises_load_error(
        self, mock_generate_report_csv, mock_load_graphic
    ):
        """
        testing function
        """

        self.mock_transform_contract.transformation_content = None

        with self.assertRaises(LoadError):
            self.loader.load_requered_files(self.mock_transform_contract)
