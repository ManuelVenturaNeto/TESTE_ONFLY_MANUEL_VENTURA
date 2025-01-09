from datetime import datetime
from src.stages.contracts.extract_contract import ExtractContract

extract_contract_mock = ExtractContract(
    raw_information_content={
        "1": {
            "name": "bulbasaur",
            "base_experience": 64,
            "types": ["grass", "poison"],
            "hp": 45,
            "attack": 49,
            "defense": 49,
        },
        "2": {
            "name": "ivysaur",
            "base_experience": 142,
            "types": ["grass", "poison"],
            "hp": 60,
            "attack": 62,
            "defense": 63,
        },
        "3": {
            "name": "venusaur",
            "base_experience": 263,
            "types": ["grass", "poison"],
            "hp": 80,
            "attack": 82,
            "defense": 83,
        },
        "4": {
            "name": "charmander",
            "base_experience": 62,
            "types": ["fire"],
            "hp": 39,
            "attack": 52,
            "defense": 43,
        },
        "5": {
            "name": "charmeleon",
            "base_experience": 142,
            "types": ["fire"],
            "hp": 58,
            "attack": 64,
            "defense": 58,
        },
    },
    extraction_date=datetime.now(),
)
