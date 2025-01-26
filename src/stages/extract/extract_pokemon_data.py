import logging
from datetime import datetime
from src.drivers.http_requester import HttpRequester
from src.stages.contracts.extract_contract import ExtractContract
from src.errors.extract_error import ExtractError
import asyncio

class ExtractPokemonData:
    """
    Class to define a collection of Pokémon
    """

    def __init__(self):
        self.http_requester = HttpRequester()
        self.log = logging.getLogger(__name__)
        self.log.debug("ExtractPokemonData Started")

    async def collect_essential_informations(self) -> ExtractContract:
        """
        Create a collection with the essential information of all pokemons
        """
        try:
            data_entry = await self.http_requester.get_100_pokemons_from_api()
            self.log.debug("Success in HttpRequester to using func: get_100_pokemons_from_api")

            all_pokemons = data_entry["informations"]["results"]
            pokemon_general_dict = {}

            self.log.debug("Start to get information of 100 Pokemons")

            tasks = []
            for pokemon in all_pokemons:
                task = self._get_pokemon_data(pokemon, pokemon_general_dict)
                tasks.append(task)

            await asyncio.gather(*tasks)

            return ExtractContract(
                raw_information_content=pokemon_general_dict,
                extraction_date=datetime.now(),
            )

        except Exception as exception:
            self.log.error("Error in ExtractContract to using func: collect_essential_informations")
            raise ExtractError(str(exception)) from exception

    async def _get_pokemon_data(self, pokemon, pokemon_general_dict):
        """
        Helper method to get individual Pokémon data asynchronously
        """
        name = pokemon["name"]
        url = pokemon["url"]
        pokemon_id = url.strip("/").split("/")[-1]

        other_informations = await self.http_requester.get_unique_pokemon_data(url=url)
        self.log.debug("Success in HttpRequester to using func: get_unique_pokemon_data")

        xp_base = other_informations.get("base_experience")
        types = [tipo["type"]["name"] for tipo in other_informations.get("types", [])]
        hp = next((stat["base_stat"] for stat in other_informations.get("stats", []) if stat["stat"]["name"] == "hp"), None)
        atack = next((stat["base_stat"] for stat in other_informations.get("stats", []) if stat["stat"]["name"] == "attack"), None)
        defence = next((stat["base_stat"] for stat in other_informations.get("stats", []) if stat["stat"]["name"] == "defense"), None)

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