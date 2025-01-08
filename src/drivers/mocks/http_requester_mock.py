# pylint: disable=line-too-long, R1710


def mock_get_100_pokemons_from_api():
    """
    funcion to mock data to simule an API access
    """
    return {
        "results": [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
            {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
        ]
    }


def mock_get_100_pokemons_from_api_for_collections():
    """
    funcion to mock data to simule an API access
    """
    return {
        "status_code": 200,
        "informations": {
            "results": [
                {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
                {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
            ]
        },
    }


def mock_get_unique_pokemon_data():
    """
    funcion to mock data to simule an API access
    """
    return {
        "abilities": [
            {
                "ability": {
                    "name": "overgrow",
                    "url": "https://pokeapi.co/api/v2/ability/65/",
                },
                "is_hidden": False,
                "slot": 1,
            },
            {
                "ability": {
                    "name": "chlorophyll",
                    "url": "https://pokeapi.co/api/v2/ability/34/",
                },
                "is_hidden": True,
                "slot": 3,
            },
        ],
        "base_experience": 64,
        "cries": {
            "latest": "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/1.ogg",
            "legacy": "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/legacy/1.ogg",
        },
        "forms": [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon-form/1/"}
        ],
        "game_indices": [],
        "height": 7,
        "held_items": [],
        "id": 1,
        "is_default": True,
        "location_area_encounters": "https://pokeapi.co/api/v2/pokemon/1/encounters",
        "moves": [],
        "name": "bulbasaur",
        "order": 1,
        "past_abilities": [],
        "past_types": [],
        "species": {
            "name": "bulbasaur",
            "url": "https://pokeapi.co/api/v2/pokemon-species/1/",
        },
        "sprites": {},
        "stats": [
            {
                "base_stat": 45,
                "effort": 0,
                "stat": {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"},
            },
            {
                "base_stat": 49,
                "effort": 0,
                "stat": {"name": "attack", "url": "https://pokeapi.co/api/v2/stat/2/"},
            },
            {
                "base_stat": 49,
                "effort": 0,
                "stat": {"name": "defense", "url": "https://pokeapi.co/api/v2/stat/3/"},
            },
            {
                "base_stat": 65,
                "effort": 1,
                "stat": {
                    "name": "special-attack",
                    "url": "https://pokeapi.co/api/v2/stat/4/",
                },
            },
            {
                "base_stat": 65,
                "effort": 0,
                "stat": {
                    "name": "special-defense",
                    "url": "https://pokeapi.co/api/v2/stat/5/",
                },
            },
            {
                "base_stat": 45,
                "effort": 0,
                "stat": {"name": "speed", "url": "https://pokeapi.co/api/v2/stat/6/"},
            },
        ],
        "types": [
            {
                "slot": 1,
                "type": {"name": "grass", "url": "https://pokeapi.co/api/v2/type/12/"},
            },
            {
                "slot": 2,
                "type": {"name": "poison", "url": "https://pokeapi.co/api/v2/type/4/"},
            },
        ],
        "weight": 69,
    }
