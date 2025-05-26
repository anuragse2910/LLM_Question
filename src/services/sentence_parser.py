class SentenceParser:
    def parse(self, sentence: str) -> str:
        # Basic validation and cleaning
        if not isinstance(sentence, str) or not sentence.strip():
            raise ValueError("Input sentence must be a non-empty string")
        return sentence.strip()