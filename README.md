# OpenRouter Chat App

A proof of concept chat application using VS Code, Cline, and OpenRouter, built with Flask.

## Overview
This project demonstrates the integration of various development tools and technologies:
- Visual Studio Code as the IDE
- Cline for AI-assisted development
- OpenRouter API for chat functionality
- Flask for the web framework

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

The application will be available at `http://localhost:5000`

## Features

- Clean, modern chat interface
- Integration with OpenRouter API
- Message history display
- Real-time chat interactions

## License

MIT License
