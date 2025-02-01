# Contributing to OpenRouter Chat App

Thank you for your interest in contributing to the OpenRouter Chat App! This document provides guidelines and instructions for contributing to the project.

## Code Style

- Python code follows PEP 8 style guide
- JavaScript uses ES6+ features and follows Modern JavaScript style guide
- CSS uses BEM naming convention for classes
- HTML follows semantic markup practices

## Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/your-username/openrouter-chat-app.git
cd openrouter-chat-app
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file with your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

## Making Changes

1. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following the code style guidelines
3. Test your changes thoroughly
4. Commit your changes with clear, descriptive commit messages
5. Push to your fork and submit a pull request

## Pull Request Guidelines

- Provide a clear description of the changes
- Include any relevant issue numbers
- Ensure all tests pass
- Follow the existing code style
- Keep changes focused and atomic

## Code Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

## Security

- Never commit API keys or sensitive data
- Use environment variables for configuration
- Follow security best practices
- Report security vulnerabilities privately

## Testing

- Add tests for new features
- Ensure existing tests pass
- Test across different browsers and devices
- Check for responsive design issues

## Documentation

- Update README.md for new features
- Add JSDoc comments for JavaScript functions
- Include docstrings for Python functions
- Document API endpoints and parameters

## Questions?

Feel free to open an issue for:
- Feature proposals
- Bug reports
- Documentation improvements
- General questions

Thank you for contributing!
