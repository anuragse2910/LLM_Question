import json
from typing import Dict, Any
from interfaces.storage_interface import StorageInterface
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent /"Data"/"questions.json"

class JsonStorage(StorageInterface):
    def __init__(self, file_path: str = DATA_PATH):
        self.file_path = file_path

    def save_question(self, question: Dict[str, Any]) -> None:
        try:
            with open(self.file_path, 'r') as f:
                questions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            questions = []
        
        questions.append(question)
        
        with open(self.file_path, 'w') as f:
            json.dump(questions, f, indent=2)