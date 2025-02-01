from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get API key from environment variable
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not OPENROUTER_API_KEY:
        return jsonify({'error': 'OpenRouter API key not found'}), 401

    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    host_url = request.host_url.rstrip('/')  # Get the current host URL
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
        'HTTP-Referer': host_url,  # Required by OpenRouter
        'OpenAI-Organization': host_url  # Required by OpenRouter
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
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        assistant_message = response.json()['choices'][0]['message']['content']
        return jsonify({'response': assistant_message})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
