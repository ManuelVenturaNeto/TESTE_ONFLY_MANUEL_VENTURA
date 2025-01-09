from src.stages.extract import ExtractPokemonData
from src.stages.transform import TransformPokemonData
from src.stages.load import LoadPokemonFiles


class MainPipeline:
    def __init__(self) -> None:
        self.__extract = ExtractPokemonData()
        self.__transform = TransformPokemonData()
        self.__load = LoadPokemonFiles()

    def run_pipeline(self) -> None:
        extract_contract = self.__extract.collect_essential_informations()
        transformed = self.__transform.tranform_pokemon_data(extract_contract)
        self.__load.load(transformed)
