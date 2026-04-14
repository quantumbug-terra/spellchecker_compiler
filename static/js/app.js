// ================================================
// ENGLISH SPELLING CORRECTION SYSTEM
// Frontend JavaScript
// ================================================

// DOM Elements
const inputText = document.getElementById('inputText');
const checkBtn = document.getElementById('checkBtn');
const clearBtn = document.getElementById('clearBtn');
const copyBtn = document.getElementById('copyBtn');

const loading = document.getElementById('loading');
const errorMsg = document.getElementById('errorMsg');
const stats = document.getElementById('stats');

const tokensSection = document.getElementById('tokensSection');
const tokensList = document.getElementById('tokensList');

const spellingSection = document.getElementById('spellingSection');
const spellingErrorsList = document.getElementById('spellingErrorsList');

const grammarSection = document.getElementById('grammarSection');
const grammarErrorsList = document.getElementById('grammarErrorsList');

const correctedSection = document.getElementById('correctedSection');
const correctedText = document.getElementById('correctedText');

// Event Listeners
checkBtn.addEventListener('click', checkText);
clearBtn.addEventListener('click', clearAll);
copyBtn.addEventListener('click', copyToClipboard);

/**
 * Main function to check text
 */
async function checkText() {
    const text = inputText.value.trim();

    // Validation
    if (!text) {
        showError('Please enter some text to check!');
        return;
    }

    // Show loading
    showLoading(true);
    hideAllResults();

    try {
        // Send request to backend
        const response = await fetch('/api/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (data.status === 'success') {
            displayResults(data);
        } else {
            showError(data.message || 'An error occurred while processing the text');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        showLoading(false);
    }
}

/**
 * Display all results
 */
function displayResults(data) {
    // Show statistics
    displayStats(data.statistics);

    // Show tokens
    if (data.tokens && data.tokens.length > 0) {
        displayTokens(data.tokens);
    }

    // Show spelling errors
    if (data.spelling_errors && data.spelling_errors.length > 0) {
        displaySpellingErrors(data.spelling_errors);
    }

    // Show grammar errors
    if (data.grammar_errors && data.grammar_errors.length > 0) {
        displayGrammarErrors(data.grammar_errors);
    }

    // Show corrected text
    if (data.corrected_text) {
        displayCorrectedText(data.corrected_text);
    }
}

/**
 * Display statistics
 */
function displayStats(stats_data) {
    document.getElementById('totalWords').textContent = stats_data.total_words;
    document.getElementById('totalErrors').textContent = stats_data.total_errors;
    document.getElementById('spellingErrors').textContent = stats_data.spelling_errors_count;
    document.getElementById('grammarErrors').textContent = stats_data.grammar_errors_count;
    
    stats.classList.remove('hidden');
}

/**
 * Display tokens (lexical analysis)
 */
function displayTokens(tokens) {
    tokensList.innerHTML = '';

    tokens.forEach((token, index) => {
        const span = document.createElement('span');
        span.className = `token ${token.type}`;
        
        // Display value with visible spaces
        let displayValue = token.value;
        if (token.type === 'WHITESPACE') {
            displayValue = '␣'; // Visible space character
        }
        
        span.textContent = `${displayValue}`;
        span.title = `Type: ${token.type}\nPosition: ${token.position}`;
        
        tokensList.appendChild(span);
    });

    tokensSection.classList.remove('hidden');
}

/**
 * Display spelling errors
 */
function displaySpellingErrors(errors) {
    spellingErrorsList.innerHTML = '';

    if (errors.length === 0) {
        const p = document.createElement('p');
        p.textContent = '✓ No spelling errors found!';
        p.style.color = 'var(--primary-color)';
        spellingErrorsList.appendChild(p);
    } else {
        errors.forEach((error, index) => {
            const div = document.createElement('div');
            div.className = 'error-item spelling';
            
            const details = document.createElement('div');
            details.className = 'error-details';
            
            let suggestionsHTML = '';
            if (error.suggestions && error.suggestions.length > 0) {
                suggestionsHTML = `
                    <div class="error-suggestion-list">
                        Suggestions: ${error.suggestions.map(s => `<span class="error-suggestion">${s}</span>`).join(', ')}
                    </div>
                `;
            }
            
            details.innerHTML = `
                <span class="error-word">"${error.word}"</span> at position ${error.position}
                ${suggestionsHTML}
            `;
            
            div.appendChild(details);
            spellingErrorsList.appendChild(div);
        });
    }

    spellingSection.classList.remove('hidden');
}

/**
 * Display grammar errors
 */
function displayGrammarErrors(errors) {
    grammarErrorsList.innerHTML = '';

    if (errors.length === 0) {
        const p = document.createElement('p');
        p.textContent = '✓ No grammar errors found!';
        p.style.color = 'var(--primary-color)';
        grammarErrorsList.appendChild(p);
    } else {
        errors.forEach((error, index) => {
            const div = document.createElement('div');
            div.className = 'error-item grammar';
            
            const details = document.createElement('div');
            details.className = 'error-details';
            details.innerHTML = `
                <strong>${error.issue}</strong>
                <div class="error-suggestion-list">
                    Word: <span class="error-word">"${error.word}"</span> 
                    → Suggestion: <span class="error-suggestion">"${error.suggestion}"</span>
                </div>
            `;
            
            div.appendChild(details);
            grammarErrorsList.appendChild(div);
        });
    }

    grammarSection.classList.remove('hidden');
}

/**
 * Display corrected text
 */
function displayCorrectedText(text) {
    correctedText.textContent = text;
    correctedSection.classList.remove('hidden');
}

/**
 * Copy corrected text to clipboard
 */
function copyToClipboard() {
    const text = correctedText.textContent;
    navigator.clipboard.writeText(text).then(() => {
        // Show feedback
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied!';
        setTimeout(() => {
            copyBtn.textContent = originalText;
        }, 2000);
    }).catch(err => {
        showError('Failed to copy text');
    });
}

/**
 * Show error message
 */
function showError(message) {
    errorMsg.textContent = message;
    errorMsg.classList.remove('hidden');
}

/**
 * Hide error message
 */
function hideError() {
    errorMsg.classList.add('hidden');
}

/**
 * Show/hide loading spinner
 */
function showLoading(show) {
    if (show) {
        loading.classList.remove('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

/**
 * Hide all result sections
 */
function hideAllResults() {
    hideError();
    stats.classList.add('hidden');
    tokensSection.classList.add('hidden');
    spellingSection.classList.add('hidden');
    grammarSection.classList.add('hidden');
    correctedSection.classList.add('hidden');
}

/**
 * Clear all inputs and results
 */
function clearAll() {
    inputText.value = '';
    hideAllResults();
    inputText.focus();
}

// Allow Enter key (Shift+Enter for new line)
inputText.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && event.ctrlKey) {
        checkText();
    }
});

// Initialize
console.log('✓ Spelling Correction System loaded');
