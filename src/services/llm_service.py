import os
import json
from typing import Dict, Any, List
from google.generativeai import GenerativeModel
from interfaces.llm_interface import LLMInterface

class GeminiLLMService(LLMInterface):
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        self.model = GenerativeModel("gemini-1.5-flash")

    def generate_leetcode_question(self, sentence: str) -> Dict[str, Any]:
        prompt = f"""
        You are a LeetCode problem creator. Given the following sentence, create a LeetCode-style programming problem in valid JSON format. The problem should include the following fields:
        - id: A unique identifier for the problem (leave as empty string, to be filled later)
        - title: A concise title for the problem
        - description: A detailed description of the problem
        - input_format: Description of the input format
        - output_format: Description of the output format
        - constraints: A list of constraints for the input
        - examples: A list of example cases, each with input, output, and explanation
        - difficulty: One of "Easy", "Medium", or "Hard"
        - edge_cases: A list of edge cases that solutions should handle
        - approaches: A list of possible solution approaches, each with name, description, time_complexity, and space_complexity

        Ensure the output is valid JSON and contains only the problem object.

        Sentence: {sentence}

        Example output:
        {{
            "id": "",
            "title": "Sum of Even Numbers",
            "description": "Given an array of integers, return the sum of all even numbers in the array.",
            "input_format": "An array of integers nums.",
            "output_format": "An integer representing the sum of all even numbers.",
            "constraints": [
                "1 <= nums.length <= 10^4",
                "-10^5 <= nums[i] <= 10^5"
            ],
            "examples": [
                {{
                    "input": "nums = [1, 2, 3, 4, 5, 6]",
                    "output": "12",
                    "explanation": "The even numbers are 2, 4, and 6. Their sum is 2 + 4 + 6 = 12."
                }}
            ],
            "difficulty": "Easy",
            "edge_cases": [
                "Empty array",
                "Array with no even numbers",
                "Array with all even numbers"
            ],
            "approaches": [
                {{
                    "name": "Linear Scan",
                    "description": "Iterate through the array and sum even numbers.",
                    "time_complexity": "O(n)",
                    "space_complexity": "O(1)"
                }}
            ]
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            question_data = json.loads(response.text.strip("```json\n").strip("```"))
            return question_data
        except Exception as e:
            print(f"Error generating question: {str(e)}")
            return {
                "id": "",
                "title": "Error",
                "description": "Failed to generate question",
                "input_format": "",
                "output_format": "",
                "constraints": [],
                "examples": [],
                "difficulty": "Easy",
                "edge_cases": [],
                "approaches": []
            }