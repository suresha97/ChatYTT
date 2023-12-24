from abc import ABC, abstractmethod
from typing import Any, List


class BaseChain(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_response(self, query: str, context: Any) -> str:
        ...


class BaseChatChain(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_response(self, query: str, chat_history: List) -> str:
        ...
