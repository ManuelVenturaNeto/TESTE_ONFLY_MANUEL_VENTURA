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
        self.log.debug("MainPipeline Initialized")

    async def run_pipeline(self) -> None:
        """
        Executes the Extract, Transform, and Load (ETL) pipeline.
        """
        try:
            # Extract stage
            self.log.debug("Starting Extract stage")
            extract_contract = await self.__extract.collect_essential_informations()
            self.log.debug("Successfully consumed API data with ExtractPokemonData")

            # Transform stage
            self.log.debug("Starting Transform stage")
            transformed =  self.__transform.tranform_pokemon_data(extract_contract)
            self.log.debug("Successfully transformed data with TransformPokemonData")

            # Load stage
            self.log.debug("Starting Load stage")
            self.__load.load_requered_files(transformed)  # Make sure this method is async if needed
            self.log.debug("Successfully generated files with LoadPokemonFiles")

        except Exception as e:
            # Log the error and re-raise the exception to propagate failure
            self.log.error(f"Pipeline execution failed: {str(e)}")
            raise e
