from typing import Dict, Any
from interfaces.llm_interface import LLMInterface
from interfaces.storage_interface import StorageInterface
from services.sentence_parser import SentenceParser
from services.question_formatter import QuestionFormatter
from models.leetcode_question import LeetCodeQuestion

class QuestionWorkflow:
    def __init__(self, llm: LLMInterface, storage: StorageInterface, parser: SentenceParser, formatter: QuestionFormatter):
        self.llm = llm
        self.storage = storage
        self.parser = parser
        self.formatter = formatter

    def generate_and_store_question(self, sentence: str) -> Dict[str, Any]:
        # Parse the input sentence
        cleaned_sentence = self.parser.parse(sentence)
        
        # Generate question using LLM
        question_data = self.llm.generate_leetcode_question(cleaned_sentence)
        
        # Format the question
        formatted_question = self.formatter.format_question(question_data)
        
        # Create LeetCodeQuestion model
        question = LeetCodeQuestion(
            id=formatted_question["id"],
            title=formatted_question["title"],
            description=formatted_question["description"],
            input_format=formatted_question["input_format"],
            output_format=formatted_question["output_format"],
            constraints=formatted_question["constraints"],
            examples=formatted_question["examples"],
            difficulty=formatted_question["difficulty"]
        )
        
        # Save to storage
        self.storage.save_question(question.to_dict())
        
        return question.to_dict()