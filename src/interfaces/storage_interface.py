from abc import ABC, abstractmethod
from typing import Dict, Any

class StorageInterface(ABC):
    @abstractmethod
    def save_question(self, question: Dict[str, Any]) -> None:
        pass