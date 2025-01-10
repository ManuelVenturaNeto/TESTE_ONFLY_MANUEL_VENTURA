# flake8: noqa: F811

import logging
import unittest
from unittest.mock import MagicMock
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from src.errors.transform_error import TransformError
from src.stages.contracts.transform_contract import (
    TransformContract,
)
from src.stages.contracts.extract_contract import ExtractContract
from src.stages.transform.transform_pokemon_data import TransformPokemonData


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestTransformPokemonData(unittest.TestCase):
    """
    class to define mock params and test functions
    """

    def setUp(self):
        """
        function to create mock data for tests
        """
        # create a mock to ExtractContract
        self.extract_contract_mock = MagicMock(spec=ExtractContract)

        # simulate the raw data of pokemons
        self.extract_contract_mock.raw_information_content = {
            "1": {
                "Id": "1",
                "Nome": "Pikachu",
                "Experiencia_Base": 112,
                "Tipos": ["electric"],
                "HP": 35,
                "Ataque": 55,
                "Defesa": 40,
            },
            "2": {
                "Id": "2",
                "Nome": "Ivysaur",
                "Experiencia_Base": 142,
                "Tipos": ["grass", "poison"],
                "HP": 60,
                "Ataque": 62,
                "Defesa": 63,
            },
            "3": {
                "Id": "3",
                "Nome": "Venusaur",
                "Experiencia_Base": 263,
                "Tipos": ["grass", "poison"],
                "HP": 80,
                "Ataque": 82,
                "Defesa": 83,
            },
        }

        self.transform_pokemon_data = TransformPokemonData()

    def test_raw_data_to_df(self):
        """
        testing function with mock data
        """

        df = self.transform_pokemon_data.raw_data_to_df(
            self.extract_contract_mock.raw_information_content
        )

        # testing type
        self.assertIsInstance(df, pd.DataFrame)

        # testing if function is getting correct information
        self.assertEqual(df["Nome"].iloc[0], "Pikachu")
        self.assertEqual(df["Id"].iloc[0], 1)
        self.assertEqual(df["Experiencia_Base"].iloc[0], 112)
        self.assertEqual(df["Categoria"].iloc[0], "Forte")

        logger.debug("Test 'raw_data_to_df' passed successfully")

    def test_generate_graphic_exp_vs_type(self):
        """
        testing function with mock data
        """
        df = pd.DataFrame(
            [
                {
                    "Id": 1,
                    "Nome": "Pikachu",
                    "Experiencia_Base": 112,
                    "Tipos": ["electric"],
                    "HP": 35,
                    "Ataque": 55,
                    "Defesa": 40,
                    "Categoria": "Médio",
                },
                {
                    "Id": 2,
                    "Nome": "Ivysaur",
                    "Experiencia_Base": 142,
                    "Tipos": ["grass", "poison"],
                    "HP": 60,
                    "Ataque": 62,
                    "Defesa": 63,
                    "Categoria": "Forte",
                },
                {
                    "Id": 3,
                    "Nome": "Venusaur",
                    "Experiencia_Base": 263,
                    "Tipos": ["grass", "poison"],
                    "HP": 80,
                    "Ataque": 82,
                    "Defesa": 83,
                    "Categoria": "Forte",
                },
            ]
        )

        graphic = self.transform_pokemon_data.generate_graphic_exp_vs_type(df)

        self.assertIsInstance(graphic, plt.Figure)

        logger.debug("Test 'generate_graphic_exp_vs_type' passed successfully")

    def test_top_5_higher_exp_base(self):
        """
        testing function with mock data
        """
        df = pd.DataFrame(
            [
                {
                    "Id": "1",
                    "Nome": "Bulbasaur",
                    "Experiencia_Base": 64,
                    "Tipos": ["grass", "poison"],
                    "HP": 45,
                    "Ataque": 49,
                    "Defesa": 49,
                    "Categoria": "Médio",
                },
                {
                    "Id": "2",
                    "Nome": "Ivysaur",
                    "Experiencia_Base": 142,
                    "Tipos": ["grass", "poison"],
                    "HP": 60,
                    "Ataque": 62,
                    "Defesa": 63,
                    "Categoria": "Forte",
                },
                {
                    "Id": "3",
                    "Nome": "Venusaur",
                    "Experiencia_Base": 263,
                    "Tipos": ["grass", "poison"],
                    "HP": 80,
                    "Ataque": 82,
                    "Defesa": 83,
                    "Categoria": "Forte",
                },
                {
                    "Id": "4",
                    "Nome": "Charmander",
                    "Experiencia_Base": 62,
                    "Tipos": ["fire"],
                    "HP": 39,
                    "Ataque": 52,
                    "Defesa": 43,
                    "Categoria": "Médio",
                },
                {
                    "Id": "5",
                    "Nome": "Charmeleon",
                    "Experiencia_Base": 142,
                    "Tipos": ["fire"],
                    "HP": 58,
                    "Ataque": 64,
                    "Defesa": 58,
                    "Categoria": "Forte",
                },
                {
                    "Id": "6",
                    "Nome": "Charizard",
                    "Experiencia_Base": 267,
                    "Tipos": ["fire", "flying"],
                    "HP": 78,
                    "Ataque": 84,
                    "Defesa": 78,
                    "Categoria": "Forte",
                },
                {
                    "Id": "7",
                    "Nome": "Squirtle",
                    "Experiencia_Base": 63,
                    "Tipos": ["water"],
                    "HP": 44,
                    "Ataque": 82,
                    "Defesa": 65,
                    "Categoria": "Médio",
                },
            ]
        )

        top_5_df = self.transform_pokemon_data.top_5_higher_exp_base(df)

        # testing if function is getting correct information
        self.assertEqual(top_5_df["Nome"].iloc[0], "Charizard")

        # verify if number of row are correct
        self.assertEqual(top_5_df.shape[0], 5)

        logger.debug("Test 'top_5_higher_exp_base' passed successfully")

    def test_mean_statistics_by_type(self):
        """
        testing function with mock data
        """
        # mock data
        df = pd.DataFrame(
            [
                {
                    "Id": "1",
                    "Nome": "bulbasaur",
                    "Experiencia_Base": 64,
                    "Tipos": ["grass", "poison"],
                    "HP": 45,
                    "Ataque": 49,
                    "Defesa": 49,
                    "Categoria": "Médio",
                },
                {
                    "Id": "2",
                    "Nome": "ivysaur",
                    "Experiencia_Base": 142,
                    "Tipos": ["grass", "poison"],
                    "HP": 60,
                    "Ataque": 62,
                    "Defesa": 63,
                    "Categoria": "Forte",
                },
                {
                    "Id": "3",
                    "Nome": "venusaur",
                    "Experiencia_Base": 263,
                    "Tipos": ["grass", "poison"],
                    "HP": 80,
                    "Ataque": 82,
                    "Defesa": 83,
                    "Categoria": "Forte",
                },
            ]
        )

        mean_stats_df = self.transform_pokemon_data.mean_statistics_by_type(df)

        # check the columns names
        self.assertTrue("HP" in mean_stats_df.columns)
        self.assertTrue("Ataque" in mean_stats_df.columns)
        self.assertTrue("Defesa" in mean_stats_df.columns)

        logger.debug("Test 'mean_statistics_by_type' passed successfully")

    def test_transform_pokemon_data(self):
        """
        testing function with mock data
        """
        transformed_data_contract = self.transform_pokemon_data.tranform_pokemon_data(
            self.extract_contract_mock
        )

        # checking if all keys of contract are correct
        self.assertIsInstance(transformed_data_contract, TransformContract)
        self.assertTrue("df" in transformed_data_contract.transformation_content)
        self.assertTrue(
            "graphic_information" in transformed_data_contract.transformation_content
        )
        self.assertTrue(
            "top_5_higher_exp_base" in transformed_data_contract.transformation_content
        )
        self.assertTrue(
            "mean_statistics_by_type"
            in transformed_data_contract.transformation_content
        )
        self.assertEqual(type(transformed_data_contract.transformation_date), datetime)

        logger.debug("Test 'tranform_pokemon_data' passed successfully")

    def test_transform_pokemon_data_exception(self):
        """
        testing function with mock data
        """
        self.extract_contract_mock.raw_information_content = None

        # testing if input has no data it raise an error
        with self.assertRaises(TransformError):
            self.transform_pokemon_data.tranform_pokemon_data(
                self.extract_contract_mock
            )

        logger.debug("Test 'TransformError' passed successfully")
