from .http_requester import HttpRequester


class PokemonCollector:
    """
    Class to define a collection os pokemon
    """

    def __init__(self):
        self.http_requester = HttpRequester()
        self.collection = {}

    def collect_essential_informations(self):
        """
        Create a collection with the essencial informations os all pokemons
        """

        entry = self.http_requester.get_100_pokemons_from_api()
        all_pokemons = entry["informations"]["results"]

        pokemon_general_dict = {}

        for pokemon in all_pokemons:

            name = pokemon["name"]
            url = pokemon["url"]
            pokemon_id = url.strip("/").split("/")[-1]
            other_informations = self.http_requester.get_unique_pokemon_data(url=url)

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
                "name": name,
                "base_experience": xp_base,
                "types": types,
                "hp": hp,
                "attack": atack,
                "defense": defence,
            }

            pokemon_general_dict[pokemon_id] = pokemon_individual_dictionary
