from typing import List, Dict, Any

class LeetCodeQuestion:
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        input_format: str,
        output_format: str,
        constraints: List[str],
        examples: List[Dict[str, Any]],
        difficulty: str,
        edge_cases: List[str] = None,
        approaches: List[Dict[str, Any]] = None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.input_format = input_format
        self.output_format = output_format
        self.constraints = constraints
        self.examples = examples
        self.difficulty = difficulty
        self.edge_cases = edge_cases or []
        self.approaches = approaches or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "input_format": self.input_format,
            "output_format": self.output_format,
            "constraints": self.constraints,
            "examples": self.examples,
            "difficulty": self.difficulty,
            "edge_cases": self.edge_cases,
            "approaches": self.approaches
        }