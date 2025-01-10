import logging
from src.stages.extract import ExtractPokemonData
from src.stages.transform import TransformPokemonData
from src.stages.load import LoadPokemonFiles


class MainPipeline:
    """
    Main pipeline class to orchestrate the Extract, Transform, and Load (ETL) stages for processing Pokémon data.
    """

    def __init__(self) -> None:
        self.__extract = ExtractPokemonData()
        self.__transform = TransformPokemonData()
        self.__load = LoadPokemonFiles()

        self.log = logging.getLogger(__name__)
        self.log.debug("HttpRequester Started")

    def run_pipeline(self) -> None:
        """
        Executes the Extract, Transform, and Load (ETL) pipeline.
        """
        extract_contract = self.__extract.collect_essential_informations()

        self.log.debug("Success to consume API data with ExtractPokemonData")

        transformed = self.__transform.tranform_pokemon_data(extract_contract)

        self.log.debug("Success to refine data with TransformPokemonData")

        self.__load.load_requered_files(transformed)

        self.log.debug("Success generate files with LoadPokemonFiles")
