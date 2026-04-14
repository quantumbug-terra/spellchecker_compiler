"""
SPELL CHECKER MODULE
Validates words against dictionary and suggests corrections
"""

from typing import List, Dict
from backend.dictionary import Dictionary


class SpellChecker:
    """Identifies and corrects spelling errors"""
    
    def __init__(self, dictionary: Dictionary):
        """
        Initialize spell checker with dictionary
        
        Args:
            dictionary: Dictionary object for word validation
        """
        self.dictionary = dictionary
    
    def check(self, tokens: List[Dict]) -> List[Dict]:
        """
        Check tokens for spelling errors
        
        Args:
            tokens: List of tokens from lexer
            
        Returns:
            List of spelling error dictionaries with:
            - 'position': character position in original text
            - 'word': the misspelled word
            - 'suggestions': list of corrections
            - 'error_type': 'unknown_word'
        """
        errors = []
        
        for token in tokens:
            # Only check WORD tokens
            if token['type'] == 'WORD':
                word = token['value']
                
                # Check if word is in dictionary
                if not self.dictionary.is_valid(word):
                    suggestions = self.dictionary.get_similar_words(word)
                    
                    errors.append({
                        'position': token['position'],
                        'word': word,
                        'suggestions': suggestions,
                        'error_type': 'unknown_word',
                        'length': token['length']
                    })
        
        return errors
    
    def correct(self, text: str, errors: List[Dict]) -> str:
        """
        Apply corrections to text
        
        For now, uses first suggestion if available
        (In Step 4, user will review and choose corrections)
        
        Args:
            text: Original text
            errors: List of spelling errors
            
        Returns:
            Corrected text (or original if no corrections)
        """
        
        if not errors:
            return text
        
        # Sort errors by position (reverse to maintain indices)
        sorted_errors = sorted(errors, key=lambda x: x['position'], reverse=True)
        
        corrected = text
        
        for error in sorted_errors:
            position = error['position']
            length = error['length']
            
            # Use first suggestion if available, otherwise keep original
            if error['suggestions']:
                replacement = error['suggestions'][0]
                corrected = corrected[:position] + replacement + corrected[position + length:]
        
        return corrected
    
    def get_accuracy(self, total_words: int, errors: int) -> float:
        """Calculate spelling accuracy percentage"""
        if total_words == 0:
            return 100.0
        return round((1 - errors / total_words) * 100, 2)


# Example usage:
if __name__ == "__main__":
    from backend.lexer import Lexer
    
    lexer = Lexer()
    dictionary = Dictionary('data/dictionary.txt')
    spell_checker = SpellChecker(dictionary)
    
    test_text = "Helo wrld, this is a tst."
    print(f"Original: {test_text}")
    
    tokens = lexer.tokenize(test_text)
    errors = spell_checker.check(tokens)
    
    print(f"\nFound {len(errors)} spelling errors:")
    for error in errors:
        print(f"  - '{error['word']}' at position {error['position']}")
        print(f"    Suggestions: {error['suggestions']}")
    
    corrected = spell_checker.correct(test_text, errors)
    print(f"\nCorrected: {corrected}")
