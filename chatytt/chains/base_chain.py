from abc import ABC, abstractmethod
from typing import Any


class BaseChain(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_response(self, query: str, context: Any) -> str:
        ...
