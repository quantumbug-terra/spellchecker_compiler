"""
ENGLISH SPELLING CORRECTION SYSTEM
Main Flask Application with File Upload
Author: Vinoth
"""
from flask import Flask, render_template, request, jsonify
import json
import os
from werkzeug.utils import secure_filename
from backend.lexer import Lexer
from backend.spell_checker import SpellChecker
from backend.grammar_checker import GrammarChecker
from backend.dictionary import Dictionary

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
dictionary = Dictionary('data/dictionary.txt')
lexer = Lexer()
spell_checker = SpellChecker(dictionary)
grammar_checker = GrammarChecker()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_file(filepath):
    """
    Extract text from uploaded file based on extension
    
    Args:
        filepath: Path to the uploaded file
        
    Returns:
        Extracted text as string
    """
    file_ext = filepath.rsplit('.', 1)[1].lower()
    
    if file_ext == 'txt':
        # Read plain text file
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    elif file_ext == 'docx':
        # Read Word document
        try:
            from docx import Document
            doc = Document(filepath)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except ImportError:
            raise Exception("python-docx library not installed. Install with: pip install python-docx")
    
    elif file_ext == 'doc':
        # For .doc files (older Word format)
        try:
            import textract
            text = textract.process(filepath).decode('utf-8')
            return text
        except ImportError:
            raise Exception("textract library not installed. Install with: pip install textract")
    
    else:
        raise Exception(f"Unsupported file format: {file_ext}")


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
        
        # Process the text
        result = process_text(text)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    API endpoint to upload and check file
    
    Request: multipart/form-data with 'file' field
    
    Response JSON:
    {
        "status": "success" or "error",
        "filename": "uploaded_file.txt",
        "original_text": "extracted text",
        "tokens": [...],
        "spelling_errors": [...],
        "grammar_errors": [...],
        "corrected_text": "fixed text",
        "statistics": {...}
    }
    """
    
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Save file securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from file
        text = extract_text_from_file(filepath)
        
        # Optional: Delete file after processing (uncomment if needed)
        # os.remove(filepath)
        
        if not text.strip():
            return jsonify({
                'status': 'error',
                'message': 'File is empty or contains no readable text'
            }), 400
        
        # Process the extracted text
        result = process_text(text)
        result['filename'] = filename
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


def process_text(text):
    """
    Common text processing function
    
    Args:
        text: Input text string
        
    Returns:
        Dictionary with analysis results
    """
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
    
    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)