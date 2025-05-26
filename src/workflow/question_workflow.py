from typing import Dict, Any, List
from interfaces.llm_interface import LLMInterface
from interfaces.storage_interface import StorageInterface
from services.sentence_parser import SentenceParser
from services.question_formatter import QuestionFormatter
from services.rag_service import RAGService
from services.vector_storage_service import VectorStorageService
from models.leetcode_question import LeetCodeQuestion

class QuestionWorkflow:
    def __init__(
        self,
        llm: LLMInterface,
        storage: StorageInterface,
        parser: SentenceParser,
        formatter: QuestionFormatter,
        rag_service: RAGService = None,
        vector_storage: VectorStorageService = None
    ):
        self.llm = llm
        self.storage = storage
        self.parser = parser
        self.formatter = formatter
        self.rag_service = rag_service or RAGService()
        self.vector_storage = vector_storage or VectorStorageService()

    def generate_and_store_question(self, sentence: str) -> Dict[str, Any]:
        cleaned_sentence = self.parser.parse(sentence)
        question_data = self.llm.generate_leetcode_question(cleaned_sentence)
        formatted_question = self.formatter.format_question(question_data)
        question = LeetCodeQuestion(
            id=formatted_question["id"],
            title=formatted_question["title"],
            description=formatted_question["description"],
            input_format=formatted_question["input_format"],
            output_format=formatted_question["output_format"],
            constraints=formatted_question["constraints"],
            examples=formatted_question["examples"],
            difficulty=formatted_question["difficulty"],
            edge_cases=formatted_question.get("edge_cases", []),
            approaches=formatted_question.get("approaches", [])
        )
        self.storage.save_question(question.to_dict())
        self.vector_storage.store_question(question.to_dict())
        return question.to_dict()

    def retrieve_questions(self, query: str, difficulty: str = None, top_k: int = 3) -> List[Dict[str, Any]]:
        return self.rag_service.retrieve_questions(query, difficulty, top_k)