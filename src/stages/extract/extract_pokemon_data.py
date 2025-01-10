import logging
from datetime import datetime
from src.drivers.http_requester import HttpRequester
from src.stages.contracts.extract_contract import ExtractContract
from src.errors.extract_error import ExtractError


class ExtractPokemonData:
    """
    Class to define a collection os pokemon
    """

    def __init__(self):
        self.http_requester = HttpRequester()

        self.log = logging.getLogger(__name__)
        self.log.debug("ExtractPokemonData Started")

    def collect_essential_informations(self) -> ExtractContract:
        """
        Create a collection with the essencial informations os all pokemons
        """

        try:
            data_entry = self.http_requester.get_100_pokemons_from_api()

            self.log.debug(
                "Success in HttpRequester to using func: get_100_pokemons_from_api"
            )

            all_pokemons = data_entry["informations"]["results"]

            pokemon_general_dict = {}

            # get necessare data of each pokemon and concentrate in a dict
            self.log.debug("Start to get informations of 100 Pokemons")
            for pokemon in all_pokemons:

                name = pokemon["name"]
                url = pokemon["url"]
                pokemon_id = url.strip("/").split("/")[-1]
                other_informations = self.http_requester.get_unique_pokemon_data(
                    url=url
                )

                self.log.debug(
                    "Success in HttpRequester to using func: get_unique_pokemon_data"
                )

                xp_base = other_informations.get("base_experience")
                types = [
                    tipo["type"]["name"] for tipo in other_informations.get("types", [])
                ]
                hp = next(
                    (
                        stat["base_stat"]
                        for stat in other_informations.get("stats", [])
                        if stat["stat"]["name"] == "hp"
                    ),
                    None,
                )
                atack = next(
                    (
                        stat["base_stat"]
                        for stat in other_informations.get("stats", [])
                        if stat["stat"]["name"] == "attack"
                    ),
                    None,
                )
                defence = next(
                    (
                        stat["base_stat"]
                        for stat in other_informations.get("stats", [])
                        if stat["stat"]["name"] == "defense"
                    ),
                    None,
                )
                pokemon_individual_dictionary = {
                    "Id": pokemon_id,
                    "Nome": name,
                    "Experiencia_Base": xp_base,
                    "Tipos": types,
                    "HP": hp,
                    "Ataque": atack,
                    "Defesa": defence,
                }

                pokemon_general_dict[pokemon_id] = pokemon_individual_dictionary

            return ExtractContract(
                raw_information_content=pokemon_general_dict,
                extraction_date=datetime.now(),
            )

        except Exception as exception:  # pylint: disable=broad-except
            self.log.error(
                "Error in ExtractContract to using func: collect_essential_informations"
            )
            raise ExtractError(str(exception)) from exception
