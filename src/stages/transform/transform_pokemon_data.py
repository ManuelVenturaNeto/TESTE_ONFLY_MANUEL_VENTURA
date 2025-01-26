from datetime import datetime
import logging
import pandas as pd
import matplotlib.pyplot as plt
from src.stages.contracts.transform_contract import TransformContract
from src.stages.contracts.extract_contract import ExtractContract
from src.errors.transform_error import TransformError


class TransformPokemonData:
    """
    Class to transform raw data to dataframe informations
    """

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.debug("TransformPokemonData Started")

    def tranform_pokemon_data(
        self, extract_contract: ExtractContract
    ) -> TransformContract:
        """
        Function to get the extract raw data and transform to refined data
        -params:  ExtractContract: a named tuple with raw data and time os generation
        -return:  TransformContract: a named tuple with refined data and time of generation
        """
        try:
            raw_data = extract_contract.raw_information_content

            df = self.raw_data_to_df(raw_data)
            self.log.debug(
                "Success in TransformPokemonData to using func: raw_data_to_df"
            )

            graphic_information = self.generate_graphic_exp_vs_type(df)
            self.log.debug(
                "Success in TransformPokemonData to using func: generate_graphic_exp_vs_type"
            )

            top_5_exp_base = self.top_5_higher_exp_base(df)
            self.log.debug(
                "Success in TransformPokemonData to using func:top_5_higher_exp_base"
            )

            mean_of_statistic = self.mean_statistics_by_type(df)
            self.log.debug(
                "Success in TransformPokemonData to using func: mean_statistics_by_type"
            )

            transform_data = {
                "df": df,
                "graphic_information": graphic_information,
                "top_5_higher_exp_base": top_5_exp_base,
                "mean_statistics_by_type": mean_of_statistic,
            }

            transformed_data_contract = TransformContract(
                transformation_content=transform_data,
                transformation_date=datetime.now(),
            )
            return transformed_data_contract

        except Exception as exception:  # pylint: disable=broad-except
            self.log.error(
                "Error in TransformPokemonData to using func: tranform_pokemon_data"
            )
            raise TransformError(str(exception)) from exception

    def raw_data_to_df(self, extract_contract) -> pd.DataFrame:
        """
        Function to transform raw data in a dataframe with correct params
        -params:  extract_contract: raw information get by extract class
        -return:  df: a dataframe with typed information
        """

        def classify_pokemon(exp) -> str:
            """
            Function to find how strong is the pokemon based in experience_base
            -params: exp - experience point of that pokemon
            -return: str: return a string describing how strong that pokemon is
            """
            if exp < 50:
                return "Fraco"
            if 50 <= exp <= 100:
                return "Médio"
            return "Forte"

        try:
            df = pd.DataFrame(extract_contract).T

            # Normalize pokemon's names
            df["Nome"] = df["Nome"].str.capitalize()

            # Guarantees that this data are int type
            int_columns = ["Id", "Experiencia_Base", "HP", "Ataque", "Defesa"]
            for col in int_columns:
                if col in df.columns:
                    # Convert to numeric first to avoid FutureWarning
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

            # Create a new column called Categoria and attributing in it how strong that pokemon is
            df["Categoria"] = df["Experiencia_Base"].apply(classify_pokemon)

            return df

        except Exception as exception:
            self.log.error(
                "Error in TransformPokemonData to using func: raw_data_to_df"
            )
            raise TransformError(str(exception)) from exception

    def generate_graphic_exp_vs_type(self, df) -> plt.Figure:
        """
        Function to generate a graphic by dataframe
        -params:  df: dataframe with pokemon informations
        -return:  plt.Figure: a graphic with distribution of exp vs type
        """
        try:
            # Collect types information in dataframe
            explode_df = df.explode("Tipos")
            tipo_count = explode_df["Tipos"].value_counts()

            # Create graphic
            grafico_pokemons_por_xp, eixos = plt.subplots()
            tipo_count.plot(
                kind="bar",
                color="skyblue",
                title="Distribuição de Pokémon por Tipo",
                ax=eixos,
            )
            eixos.set_xlabel("Tipo")
            eixos.set_ylabel("Quantidade")
            plt.tight_layout()

            return grafico_pokemons_por_xp

        except Exception as exception:
            self.log.error(
                "Error in TransformPokemonData to using func: generate_graphic_exp_vs_type"
            )
            raise TransformError(str(exception)) from exception

    def top_5_higher_exp_base(self, df) -> pd.DataFrame:
        """
        Function to generate table with pokemon with higher experience base
        -params:  df: dataframe with pokemon informations
        -return:  pd.DataFrame: a dataframe with only 5 pokemons with higher exp
        """
        try:
            top_5_exp_base = df.sort_values(
                by=["Experiencia_Base", "Id"], ascending=[False, True]
            ).head(5)
            return top_5_exp_base
        except Exception as exception:
            self.log.error(
                "Error in TransformPokemonData to using func: top_5_higher_exp_base"
            )
            raise TransformError(str(exception)) from exception

    def mean_statistics_by_type(self, df) -> pd.DataFrame:
        """
        Function to generate a table with the mean statistics (HP, Ataque, Defesa) of each Pokémon type.
        -params:  df: dataframe with pokemon informations
        -return:  pd.DataFrame: A DataFrame with the mean statistics (HP, Ataque, Defesa) for each Pokémon type.
        """
        try:
            explode_df = df.explode("Tipos")

            mean_by_type = (
                explode_df.groupby("Tipos")[["HP", "Ataque", "Defesa"]].mean().round(2)
            )

            return mean_by_type
        except Exception as exception:
            self.log.error(
                "Error in TransformPokemonData to using func: mean_statistics_by_type"
            )
            raise TransformError(str(exception)) from exception