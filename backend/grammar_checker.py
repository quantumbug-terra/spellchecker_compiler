"""
GRAMMAR CHECKER MODULE
Validates basic grammar rules
"""

from typing import List, Dict


class GrammarChecker:
    """Checks for basic grammar errors"""
    
    def __init__(self):
        """Initialize grammar rules"""
        self.rules = {
            'capitalization': self._check_capitalization,
            'articles': self._check_articles,
            'punctuation': self._check_punctuation_spacing,
            'subject_verb': self._check_subject_verb,
        }
    
    def check(self, tokens: List[Dict]) -> List[Dict]:
        """
        Check tokens for grammar errors
        
        Args:
            tokens: List of tokens from lexer
            
        Returns:
            List of grammar error dictionaries with:
            - 'position': character position
            - 'issue': description of grammar error
            - 'suggestion': recommended fix
            - 'error_type': type of grammar error
        """
        errors = []
        
        # Check each rule
        for rule_name, rule_func in self.rules.items():
            rule_errors = rule_func(tokens)
            errors.extend(rule_errors)
        
        return errors
    
    def _check_capitalization(self, tokens: List[Dict]) -> List[Dict]:
        """
        Check capitalization rules:
        - First word of sentence should be capitalized
        - Proper nouns (heuristic)
        """
        errors = []
        
        for i, token in enumerate(tokens):
            if token['type'] == 'WORD':
                word = token['value']
                
                # First word of text should be capitalized
                if i == 0 and word[0].islower():
                    errors.append({
                        'position': token['position'],
                        'issue': 'First word should be capitalized',
                        'word': word,
                        'suggestion': word.capitalize(),
                        'error_type': 'capitalization',
                        'severity': 'minor'
                    })
                
                # Word after period should be capitalized
                if i > 0:
                    prev_token = tokens[i - 1]
                    if prev_token['type'] == 'PUNCTUATION' and prev_token['value'] == '.':
                        if word[0].islower():
                            errors.append({
                                'position': token['position'],
                                'issue': 'Word after period should be capitalized',
                                'word': word,
                                'suggestion': word.capitalize(),
                                'error_type': 'capitalization',
                                'severity': 'minor'
                            })
        
        return errors
    
    def _check_articles(self, tokens: List[Dict]) -> List[Dict]:
        """
        Check article usage (a/an)
        - Use 'an' before vowels
        - Use 'a' before consonants
        """
        errors = []
        vowels = 'aeiouAEIOU'
        
        for i, token in enumerate(tokens):
            if token['type'] == 'WORD' and token['value'].lower() in ['a', 'an']:
                article = token['value'].lower()
                
                # Look at next word
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    
                    if next_token['type'] == 'WORD':
                        next_word = next_token['value']
                        first_char = next_word[0]
                        
                        if article == 'a' and first_char in vowels:
                            errors.append({
                                'position': token['position'],
                                'issue': f"Use 'an' before vowel '{first_char}'",
                                'word': article,
                                'suggestion': 'an',
                                'error_type': 'articles',
                                'severity': 'minor'
                            })
                        
                        elif article == 'an' and first_char not in vowels:
                            errors.append({
                                'position': token['position'],
                                'issue': f"Use 'a' before consonant '{first_char}'",
                                'word': article,
                                'suggestion': 'a',
                                'error_type': 'articles',
                                'severity': 'minor'
                            })
        
        return errors
    
    def _check_punctuation_spacing(self, tokens: List[Dict]) -> List[Dict]:
        """Check spacing around punctuation"""
        errors = []
        
        for i, token in enumerate(tokens):
            if token['type'] == 'PUNCTUATION':
                # No space before period, comma, etc.
                if i > 0 and tokens[i - 1]['type'] == 'WHITESPACE':
                    errors.append({
                        'position': token['position'],
                        'issue': f"No space before '{token['value']}'",
                        'word': token['value'],
                        'suggestion': token['value'],
                        'error_type': 'punctuation_spacing',
                        'severity': 'minor'
                    })
        
        return errors
    
    def _check_subject_verb(self, tokens: List[Dict]) -> List[Dict]:
        """
        Check subject-verb agreement (basic)
        This is simplified - full implementation would need parsing
        """
        errors = []
        
        # Placeholder for more complex grammar checking
        # In a real implementation, you'd parse the sentence structure
        
        return errors


# Example usage:
if __name__ == "__main__":
    from backend.lexer import Lexer
    
    lexer = Lexer()
    grammar_checker = GrammarChecker()
    
    test_text = "hello world. this is a test."
    print(f"Text: {test_text}")
    
    tokens = lexer.tokenize(test_text)
    errors = grammar_checker.check(tokens)
    
    print(f"\nFound {len(errors)} grammar errors:")
    for error in errors:
        print(f"  - {error['issue']}")
        print(f"    Position: {error['position']}, Word: '{error['word']}'")
        print(f"    Suggestion: '{error['suggestion']}'")
