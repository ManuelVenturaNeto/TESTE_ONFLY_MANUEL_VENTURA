import os
import logging
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from src.stages.contracts.transform_contract import TransformContract
from src.errors.load_error import LoadError


class LoadPokemonFiles:
    """
    Class to load pokemon files in output file
    """

    def __init__(self):

        self.log = logging.getLogger(__name__)
        self.log.debug("LoadPokemonFiles Started")

    def load_requered_files(self, transform_contract: TransformContract) -> None:
        """
        Function to get refined data and load into outputs file on project root
        -params:  TransformContract: a named tuple with refined data and time of generation
        -return:  None
        """
        try:
            informations = transform_contract.transformation_content

            graphic = informations["graphic_information"]
            top_5_exp_base = informations["top_5_higher_exp_base"]
            mean_of_statistic = informations["mean_statistics_by_type"]

            self.load_graphic_bar_by_type(graphic)

            self.log.debug(
                "Success in LoadPokemonFiles to using func: load_graphic_bar_by_type"
            )

            self.generate_report_csv(top_5_exp_base, mean_of_statistic)

            self.log.debug(
                "Success in LoadPokemonFiles to using func: generate_report_csv"
            )

        except Exception as exception:  # pylint: disable=broad-except
            self.log.error(
                "Error in LoadPokemonFiles to using func: load_requered_files"
            )
            raise LoadError(str(exception)) from exception

    def load_graphic_bar_by_type(self, graphic: plt.Figure) -> None:
        """
        Function to receive the graphic and sabe it on the root
        """
        try:
            # define diretory
            output_dir = os.path.join(os.getcwd(), "outputs")

            # create the directory if it do not exist
            os.makedirs(output_dir, exist_ok=True)

            # give a name to file
            output_path = os.path.join(
                output_dir,
                f"pokemon_tipo_distribuicao{datetime.now().strftime('_%Y-%m-%d_%H-%M')}.png",
            )

            # save file
            graphic.savefig(output_path, format="png", dpi=300)

            # close file
            # plt.close(graphic)
        except:
            self.log.error(
                "Error in LoadPokemonFiles to using func: load_graphic_bar_by_type"
            )

    def generate_report_csv(
        self, top_5_exp_base: pd.DataFrame, mean_of_statistic: pd.DataFrame
    ) -> None:
        """
        Generate a CSV report with the following information:
        - Top 5 Pokémon with the highest base experience.
        - Mean statistics of HP, Attack, and Defense.
        - Distribution of base experience by type (as a graph reference).
        """
        # Prepare the report content
        try:

            report_data = {
                "Top_5_Exp_Base": [
                    top_5_exp_base[
                        ["Id", "Nome", "Experiencia_Base", "Tipos"]
                    ].to_string(index=False)
                ],
                "Mean_Stats": [mean_of_statistic.to_string(index=False)],
                "Graphic_Reference": ["outputs/pokemon_tipo_distribuicao.png"],
            }

            # Convert report data to DataFrame for better structure
            report_df = pd.DataFrame(report_data)

            # Define the output directory and file name
            output_dir = os.path.join(os.getcwd(), "outputs")
            os.makedirs(output_dir, exist_ok=True)

            # Define the output file path
            report_path = os.path.join(
                output_dir,
                f"pokemon_report_{datetime.now().strftime('_%Y-%m-%d_%H-%M')}.csv",
            )

            # Save the DataFrame to CSV
            report_df.to_csv(report_path, index=False)
        except:
            self.log.error(
                "Error in LoadPokemonFiles to using func: generate_report_csv"
            )
