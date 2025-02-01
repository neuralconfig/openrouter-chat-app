# OpenRouter Chat App

A sophisticated chat application that demonstrates integration of modern AI capabilities through OpenRouter's API, built with Flask and modern web technologies.

## Technical Architecture
- Frontend: HTML, CSS, JavaScript for a responsive single-page application
- Backend: Flask (Python) providing a RESTful API interface
- AI Integration: OpenRouter API for advanced chat capabilities
- Security: Environment-based configuration and CORS protection
- Error Handling: Comprehensive error management for API interactions

## Tech Stack
- Python 3.x
- Flask 3.0.0
- Flask-CORS 4.0.0
- OpenRouter API (Claude 3.5 Haiku model)
- Modern JavaScript (ES6+)

## Project Structure
```
├── app.py              # Main Flask application
├── static/            
│   ├── css/           # Styling
│   └── js/            # Frontend JavaScript
├── templates/         # HTML templates
├── requirements.txt   # Python dependencies
└── .env              # Environment variables (not tracked)
```

## Key Features
- Clean, modern chat interface with responsive design
- Real-time message handling and display
- Robust error handling and user feedback
- Secure API key management
- Cross-Origin Resource Sharing (CORS) enabled
- Configurable AI model parameters

## API Implementation
### Endpoints
- GET `/`: Serves the main chat interface
- POST `/chat`: Handles chat messages
  - Request body: `{ "message": "user message" }`
  - Response: `{ "response": "assistant response" }`
  - Error Handling: Comprehensive error responses for API key, network, and message validation issues

## Security Features
- Environment-based configuration for sensitive data
- No hardcoded credentials
- Request validation and sanitization
- Proper error handling to prevent information leakage
- CORS configuration for controlled access

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd openrouter-chat-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5001`

## Technical Highlights
- **Scalable Architecture**: Separation of concerns between frontend and backend
- **Error Handling**: Comprehensive error management for API interactions
- **Security Best Practices**: Environment variables, input validation, and proper CORS configuration
- **Clean Code**: Well-organized structure and modular design
- **Modern JavaScript**: ES6+ features for frontend functionality
- **Responsive Design**: Mobile-friendly interface

## Performance Considerations
- Efficient message handling
- Optimized API requests
- Minimal dependencies
- Configurable token limits and temperature settings

## Error Handling
- API key validation
- Network error management
- Input validation
- Graceful error presentation to users

## License
MIT License
