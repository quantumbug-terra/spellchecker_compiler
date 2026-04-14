"""
ENGLISH SPELLING CORRECTION SYSTEM
Main Flask Application
Author: Vinoth
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from backend.lexer import Lexer
from backend.spell_checker import SpellChecker
from backend.grammar_checker import GrammarChecker
from backend.dictionary import Dictionary

app = Flask(__name__)

# Initialize components
dictionary = Dictionary('data/dictionary.txt')
lexer = Lexer()
spell_checker = SpellChecker(dictionary)
grammar_checker = GrammarChecker()


@app.route('/')
def home():
    """Render the main web interface"""
    return render_template('index.html')


@app.route('/api/check', methods=['POST'])
def check_spelling():
    """
    API endpoint to check spelling and grammar
    
    Request JSON:
    {
        "text": "user input text"
    }
    
    Response JSON:
    {
        "status": "success" or "error",
        "original_text": "user input",
        "tokens": [...],
        "spelling_errors": [...],
        "grammar_errors": [...],
        "corrected_text": "fixed text",
        "statistics": {...}
    }
    """
    
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'status': 'error',
                'message': 'Please enter some text'
            }), 400
        
        # Step 1: Lexical Analysis (tokenize text)
        tokens = lexer.tokenize(text)
        
        # Step 2: Spelling Check
        spelling_errors = spell_checker.check(tokens)
        
        # Step 3: Grammar Check
        grammar_errors = grammar_checker.check(tokens)
        
        # Step 4: Generate corrected text
        corrected_text = spell_checker.correct(text, spelling_errors)
        
        # Step 5: Compile results
        result = {
            'status': 'success',
            'original_text': text,
            'tokens': tokens,
            'spelling_errors': spelling_errors,
            'grammar_errors': grammar_errors,
            'corrected_text': corrected_text,
            'statistics': {
                'total_words': len([t for t in tokens if t['type'] == 'WORD']),
                'total_errors': len(spelling_errors) + len(grammar_errors),
                'spelling_errors_count': len(spelling_errors),
                'grammar_errors_count': len(grammar_errors)
            }
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
