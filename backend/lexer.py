"""
LEXER (Lexical Analyzer)
Converts raw text into tokens

Token types:
- WORD: alphabetic characters
- NUMBER: numeric characters
- PUNCTUATION: . , ! ? ; : " ' ( ) etc.
- WHITESPACE: spaces, tabs, newlines
- SYMBOL: special characters like @, #, $, etc.
"""

import re
from typing import List, Dict


class Lexer:
    """Tokenizes input text into a stream of tokens"""
    
    def __init__(self):
        # Define token patterns (regex)
        self.patterns = [
            ('WORD', r'[a-zA-Z]+'),
            ('NUMBER', r'\d+'),
            ('PUNCTUATION', r'[.,!?;:\'"()\-–—]'),
            ('SYMBOL', r'[@#$%^&*=+<>/\\|~`]'),
            ('WHITESPACE', r'[\s]+'),
        ]
    
    def tokenize(self, text: str) -> List[Dict]:
        """
        Tokenize input text
        
        Args:
            text: Raw input string
            
        Returns:
            List of token dictionaries with:
            - 'value': the actual token string
            - 'type': token classification (WORD, PUNCTUATION, etc.)
            - 'position': character position in original text
            - 'length': length of token
        """
        
        tokens = []
        position = 0
        
        while position < len(text):
            matched = False
            
            # Try to match each pattern at current position
            for token_type, pattern in self.patterns:
                regex = re.compile(pattern)
                match = regex.match(text, position)
                
                if match:
                    value = match.group(0)
                    tokens.append({
                        'value': value,
                        'type': token_type,
                        'position': position,
                        'length': len(value)
                    })
                    position = match.end()
                    matched = True
                    break
            
            # If no pattern matched, consume one character as UNKNOWN
            if not matched:
                tokens.append({
                    'value': text[position],
                    'type': 'UNKNOWN',
                    'position': position,
                    'length': 1
                })
                position += 1
        
        return tokens


# Example usage:
if __name__ == "__main__":
    lexer = Lexer()
    
    test_text = "Hello, world! How are you?"
    tokens = lexer.tokenize(test_text)
    
    for token in tokens:
        print(f"{token['type']:12} | {token['value']!r:15} | pos: {token['position']}")
