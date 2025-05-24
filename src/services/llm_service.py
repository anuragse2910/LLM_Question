from typing import Dict, Any
from interfaces.llm_interface import LLMInterface
import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class GeminiLLMService(LLMInterface):
    def __init__(self, api_key: str = os.getenv("GOOGLE_API_KEY")):
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_leetcode_question(self, sentence: str) -> Dict[str, Any]:
        prompt = f"""
        You are a programming problem generator. Convert the following sentence into a LeetCode-style programming problem and return the result as a valid JSON object. The response must contain ONLY the JSON object, with no additional text, markdown, code blocks (e.g., ```json), or explanations outside the JSON. The JSON must include the following fields: title, description, input_format, output_format, constraints (as a list of strings), examples (as a list of objects with input, output, and explanation fields), and difficulty (Easy, Medium, or Hard). The problem must be clear, concise, and follow LeetCode conventions.

        Sentence: {sentence}

        Example JSON output:
        {{
            "title": "Example Problem",
            "description": "Description of the problem.",
            "input_format": "Description of input.",
            "output_format": "Description of output.",
            "constraints": ["Constraint 1", "Constraint 2"],
            "examples": [
                {{
                    "input": "Example input",
                    "output": "Example output",
                    "explanation": "Explanation of the example"
                }}
            ],
            "difficulty": "Easy"
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Attempt to extract JSON if wrapped in code blocks
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
            
            # Parse the response as JSON
            try:
                return json.loads(response_text)
            except json.JSONDecodeError as e:
                # Log the raw response for debugging
                print(f"Raw Gemini API response: {response_text}")
                raise ValueError(f"Gemini API returned invalid JSON: {str(e)}")
        except Exception as e:
            raise ValueError(f"Gemini API request failed: {str(e)}")