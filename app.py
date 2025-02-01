from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from functools import wraps
import os
import requests
import time
from werkzeug.middleware.proxy_fix import ProxyFix

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Constants
MAX_MESSAGE_LENGTH = 2000
RATE_LIMIT_MESSAGES = 50  # messages
RATE_LIMIT_WINDOW = 3600  # seconds (1 hour)

def rate_limit(f):
    """Rate limiting decorator for API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not app.config.get('TESTING', False):
            # Get client IP
            ip = request.remote_addr
            current_time = time.time()
            
            if 'rate_limits' not in app.config:
                app.config['rate_limits'] = {}
            
            # Initialize or clean up old rate limit data
            if ip not in app.config['rate_limits']:
                app.config['rate_limits'][ip] = {'count': 0, 'window_start': current_time}
            elif current_time - app.config['rate_limits'][ip]['window_start'] >= RATE_LIMIT_WINDOW:
                app.config['rate_limits'][ip] = {'count': 0, 'window_start': current_time}
            
            # Check rate limit
            if app.config['rate_limits'][ip]['count'] >= RATE_LIMIT_MESSAGES:
                return jsonify({
                    'error': 'Rate limit exceeded. Please try again later.'
                }), 429
            
            # Increment counter
            app.config['rate_limits'][ip]['count'] += 1
        return f(*args, **kwargs)
    return decorated_function

# Get API key from environment variable
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def validate_message(message):
    """
    Validate the user message.
    
    Args:
        message (str): The message to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not message:
        return False, "Message cannot be empty"
    if len(message) > MAX_MESSAGE_LENGTH:
        return False, f"Message exceeds maximum length of {MAX_MESSAGE_LENGTH} characters"
    if not isinstance(message, str):
        return False, "Message must be a string"
    return True, None

@app.route('/')
def home():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
@rate_limit
def chat():
    """
    Handle chat messages and interact with OpenRouter API.
    
    Returns:
        JSON response containing either the assistant's message or an error
    """
    # Check API key
    if not OPENROUTER_API_KEY:
        return jsonify({'error': 'OpenRouter API key not found'}), 401

    # Validate request
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.json
    user_message = data.get('message', '')

    # Validate message
    is_valid, error_message = validate_message(user_message)
    if not is_valid:
        return jsonify({'error': error_message}), 400

    # Prepare request
    host_url = request.host_url.rstrip('/')
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
        'HTTP-Referer': host_url,
        'OpenAI-Organization': host_url,
        'X-Request-ID': request.headers.get('X-Request-ID', ''),
        'User-Agent': 'OpenRouterChatApp/1.0'
    }

    payload = {
        'model': 'anthropic/claude-3.5-haiku-20241022:beta',
        'messages': [
            {'role': 'user', 'content': user_message}
        ],
        'max_tokens': 1000,
        'temperature': 0.7,
        'route': 'fallback'
    }

    try:
        # Make request to OpenRouter
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        # Extract and return response
        assistant_message = response.json()['choices'][0]['message']['content']
        return jsonify({
            'response': assistant_message,
            'status': 'success'
        })

    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request timed out. Please try again.',
            'status': 'error'
        }), 504
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500
    except Exception as e:
        # Catch any other exceptions
        return jsonify({
            'error': 'An unexpected error occurred',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    # Production settings
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    app.run(host='0.0.0.0', port=5001, debug=False)
