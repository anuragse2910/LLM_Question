from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMInterface(ABC):
    @abstractmethod
    def generate_leetcode_question(self, sentence: str) -> Dict[str, Any]:
        pass