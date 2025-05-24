import uuid
from typing import Dict, Any

class QuestionFormatter:
    def format_question(self, question: Dict[str, Any]) -> Dict[str, Any]:
        formatted = question.copy()
        formatted["id"] = str(uuid.uuid4())
        return formatted