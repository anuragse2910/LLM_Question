from typing import List, Dict, Any
from services.vector_storage_service import VectorStorageService
from google.generativeai import GenerativeModel
import json
import os

class RAGService:
    def __init__(self, vector_storage: VectorStorageService = None):
        self.vector_storage = vector_storage or VectorStorageService()
        api_key = os.getenv("GOOGLE_API_KEY")
        self.model = GenerativeModel("gemini-1.5-flash") if api_key else None

    def retrieve_questions(self, query: str, difficulty: str = None, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve questions and refine with Gemini."""
        retrieved = self.vector_storage.retrieve_questions(query, difficulty, top_k)
        if not retrieved or not self.model:
            return retrieved

        return self.augment_with_llm(query, retrieved)

    def augment_with_llm(self, query: str, retrieved: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Refine retrieved questions with Gemini."""
        prompt = f"""
        You are a programming problem assistant. Given a user query and a list of retrieved LeetCode-style questions, refine the questions to ensure they are relevant to the query. Return a JSON array of up to 3 questions, each with fields: id, title, description, input_format, output_format, constraints, examples, difficulty, edge_cases, and approaches. Ensure the output is valid JSON and contains only the array.

        Query: {query}

        Retrieved questions:
        {json.dumps(retrieved, indent=2)}

        Example output:
        [
            {{
                "id": "1",
                "title": "Example Problem",
                "description": "Description of the problem.",
                "input_format": "Description of input.",
                "output_format": "Description of output.",
                "constraints": ["Constraint 1"],
                "examples": [
                    {{
                        "input": "Example input",
                        "output": "Example output",
                        "explanation": "Explanation"
                    }}
                ],
                "difficulty": "Easy",
                "edge_cases": ["Empty input"],
                "approaches": [
                    {{
                        "name": "Solution",
                        "description": "Description",
                        "time_complexity": "O(n)",
                        "space_complexity": "O(1)"
                    }}
                ]
            }}
        ]
        """
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text.strip("```json\n").strip("```"))
        except Exception as e:
            print(f"LLM augmentation failed: {str(e)}")
            return retrieved