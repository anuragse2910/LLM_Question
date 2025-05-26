import json
from services.sentence_parser import SentenceParser
from services.llm_service import GeminiLLMService
from services.question_formatter import QuestionFormatter
from services.rag_service import RAGService
from services.vector_storage_service import VectorStorageService
from storage.json_storage import JsonStorage
from workflow.question_workflow import QuestionWorkflow

def main():
    # Initialize dependencies
    llm = GeminiLLMService()
    storage = JsonStorage("questions.json")
    parser = SentenceParser()
    formatter = QuestionFormatter()
    vector_storage = VectorStorageService()
    rag_service = RAGService(vector_storage)
    workflow = QuestionWorkflow(llm, storage, parser, formatter, rag_service, vector_storage)
    
    # Example 1: Generate and store a new question
    sentence = "Given a list of numbers, find the sum of all even numbers"
    print("Generating new question:")
    result = workflow.generate_and_store_question(sentence)
    print(json.dumps(result, indent=2))
    
    # Example 2: Retrieve questions by topic
    topic = "sum"
    print(f"\nRetrieving questions for topic: {topic}")
    retrieved = workflow.retrieve_questions(topic)
    print(json.dumps(retrieved, indent=2))
    
    # Example 3: Retrieve questions by topic and difficulty
    topic = "linked lists"
    difficulty = "Hard"
    print(f"\nRetrieving questions for topic: {topic}, difficulty: {difficulty}")
    retrieved = workflow.retrieve_questions(topic, difficulty)
    print(json.dumps(retrieved, indent=2))

if __name__ == "__main__":
    main()