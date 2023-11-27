from abc import ABC, abstractmethod
from typing import Optional


class BaseChain(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_response(self, query: str, context: Optional[str] = None) -> str:
        ...
