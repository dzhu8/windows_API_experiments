from typing import Optional

class TextProcessor:
    @staticmethod
    def process_text(text: str) -> Optional[str]:
        """
        Processes the input text by removing the first word.
        Returns None if text is empty or contains only one word.
        """
        if not text:
            return None

        # Split text into words
        words = text.strip().split()
        
        if len(words) <= 1:
            return None

        # Join all words except the first one
        return ' '.join(words[1:])

    @staticmethod
    def validate_text(text: Optional[str]) -> bool:
        """
        Validates if the text is suitable for processing.
        Returns True if text is valid, False otherwise.
        """
        if text is None:
            return False
        
        text = text.strip()
        if not text or len(text.split()) < 2:
            return False
            
        return True
