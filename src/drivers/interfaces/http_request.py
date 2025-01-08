from typing import Dict
from abc import ABC, abstractmethod


class HttpRequesterInterface(ABC):

    @abstractmethod
    def get_100_pokemons_from_api(self) -> Dict[int, Dict]:
        pass
