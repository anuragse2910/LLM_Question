from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import json

class VectorStorageService:
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir, settings=Settings())
        self.collection = self.client.get_or_create_collection(name="leetcode_questions")
        self.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def store_question(self, question: Dict[str, Any]) -> None:
        """Store a question in ChromaDB."""
        try:
            # Create text for embedding
            text = f"{question['title']} {question['description']}"
            for edge_case in question.get('edge_cases', []):
                text += f" {edge_case}"
            for approach in question.get('approaches', []):
                text += f" {approach['name']} {approach['description']}"

            # Generate embedding
            embedding = self.embed_model.get_text_embedding(text)

            # Store in ChromaDB
            self.collection.upsert(
                ids=[question["id"]],
                embeddings=[embedding],
                documents=[json.dumps(question)],
                metadatas=[{"difficulty": question["difficulty"]}]
            )
        except Exception as e:
            print(f"Error storing question: {str(e)}")

    def retrieve_questions(self, query: str, difficulty: str = None, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve questions from ChromaDB."""
        try:
            # Generate query embedding
            query_embedding = self.embed_model.get_text_embedding(query)

            # Query ChromaDB
            where = {"difficulty": difficulty} if difficulty else None
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where
            )

            # Extract questions
            questions = []
            for doc in results["documents"][0]:
                questions.append(json.loads(doc))
            return questions
        except Exception as e:
            print(f"Error retrieving questions: {str(e)}")
            return []