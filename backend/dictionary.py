"""
DICTIONARY MODULE
Loads common English words and provides lookup functionality
"""

import os
from typing import Set, List


class Dictionary:
    """Manages the dictionary of valid English words"""
    
    def __init__(self, dictionary_file: str):
        """
        Initialize dictionary from file
        
        Args:
            dictionary_file: Path to dictionary.txt
        """
        self.words = set()
        self.load_dictionary(dictionary_file)
    
    def load_dictionary(self, file_path: str):
        """Load words from dictionary file"""
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        word = line.strip().lower()
                        if word:  # Only add non-empty lines
                            self.words.add(word)
                print(f"✓ Dictionary loaded: {len(self.words)} words")
            else:
                print(f"⚠ Dictionary file not found: {file_path}")
                # Load default minimal dictionary
                self._load_default_dictionary()
        
        except Exception as e:
            print(f"✗ Error loading dictionary: {e}")
            self._load_default_dictionary()
    
    def _load_default_dictionary(self):
        """Load a minimal default dictionary"""
        default_words = {
            'hello', 'world', 'how', 'are', 'you', 'i', 'am', 'is', 'are',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'from', 'for', 'with', 'by', 'of', 'about', 'into', 'through',
            'during', 'before', 'after', 'above', 'below', 'between', 'under',
            'again', 'further', 'then', 'once', 'here', 'there', 'when',
            'where', 'why', 'how', 'all', 'both', 'each', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
            'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just',
            'do', 'does', 'did', 'have', 'has', 'had', 'having', 'be',
            'being', 'been', 'be', 'should', 'would', 'could', 'ought',
            'may', 'might', 'must', 'shall', 'should', 'will', 'would',
            'this', 'that', 'these', 'those', 'what', 'which', 'who',
            'whom', 'whose', 'positive', 'negative', 'neutral', 'good',
            'bad', 'better', 'best', 'worst', 'great', 'small', 'big',
            'long', 'short', 'high', 'low', 'fast', 'slow', 'quick',
            'spelling', 'correction', 'system', 'english', 'words',
            'text', 'input', 'output', 'analysis', 'check', 'correct',
            'grammar', 'syntax', 'error', 'valid', 'invalid'
        }
        self.words.update(default_words)
        print(f"⚠ Using default dictionary: {len(self.words)} words")
    
    def is_valid(self, word: str) -> bool:
        """
        Check if a word is in the dictionary
        
        Args:
            word: Word to check
            
        Returns:
            True if word is valid, False otherwise
        """
        return word.lower() in self.words
    
    def get_similar_words(self, word: str, max_suggestions: int = 5) -> List[str]:
        """
        Find similar words (spell suggestions)
        
        Simple algorithm: words that differ by 1 character
        (You can improve this later with Levenshtein distance)
        
        Args:
            word: Misspelled word
            max_suggestions: Max number of suggestions to return
            
        Returns:
            List of suggested correct words
        """
        suggestions = []
        word = word.lower()
        
        # Only suggest from dictionary
        # For now, return top words that match first letters
        for dict_word in self.words:
            if dict_word[0] == word[0] and len(dict_word) >= len(word) - 1:
                suggestions.append(dict_word)
            if len(suggestions) >= max_suggestions:
                break
        
        return sorted(suggestions)[:max_suggestions]
    
    def add_word(self, word: str):
        """Add a word to the dictionary"""
        self.words.add(word.lower())
    
    def remove_word(self, word: str):
        """Remove a word from the dictionary"""
        self.words.discard(word.lower())
    
    def get_size(self) -> int:
        """Get total number of words in dictionary"""
        return len(self.words)


# Example usage:
if __name__ == "__main__":
    # Create dummy dictionary for testing
    dict_obj = Dictionary('data/dictionary.txt')
    
    print("\nTesting Dictionary:")
    print(f"Is 'hello' valid? {dict_obj.is_valid('hello')}")
    print(f"Is 'xyzabc' valid? {dict_obj.is_valid('xyzabc')}")
    print(f"Suggestions for 'helo': {dict_obj.get_similar_words('helo')}")
