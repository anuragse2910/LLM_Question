import json
from services.llm_service import GeminiLLMService
from services.sentence_parser import SentenceParser
from services.question_formatter import QuestionFormatter
from storage.json_storage import JsonStorage
from workflow.question_workflow import QuestionWorkflow

def main():
    # Initialize dependencies
    llm = GeminiLLMService()
    storage = JsonStorage("questions.json")
    parser = SentenceParser()
    formatter = QuestionFormatter()
    
    # Initialize workflow
    workflow = QuestionWorkflow(llm, storage, parser, formatter)
    
    # Example input sentence
    sentence = "Given a list of numbers, find the sum of all even numbers"
    
    # Run workflow
    result = workflow.generate_and_store_question(sentence)
    
    # Print result
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()