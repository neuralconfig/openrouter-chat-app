import unittest
from unittest.mock import patch, MagicMock
import json
import os
from app import app, validate_message, rate_limit

class TestChatApp(unittest.TestCase):
    def setUp(self):
        """Set up test client and environment"""
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Ensure we have a test API key
        os.environ['OPENROUTER_API_KEY'] = 'test_key'
        # Initialize rate limits in config
        app.config['rate_limits'] = {}

    def test_home_route(self):
        """Test the home route returns HTML"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)

    def test_message_validation(self):
        """Test message validation function"""
        # Test empty message
        is_valid, error = validate_message('')
        self.assertFalse(is_valid)
        self.assertEqual(error, 'Message cannot be empty')

        # Test message too long
        long_message = 'a' * 2001
        is_valid, error = validate_message(long_message)
        self.assertFalse(is_valid)
        self.assertIn('exceeds maximum length', error)

        # Test valid message
        is_valid, error = validate_message('Hello, world!')
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_chat_endpoint_validation(self):
        """Test input validation in chat endpoint"""
        # Test missing message
        response = self.client.post('/chat',
                                  data=json.dumps({}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test message too long
        long_message = {'message': 'a' * 2001}
        response = self.client.post('/chat',
                                  data=json.dumps(long_message),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    @patch('app.requests.post')
    def test_successful_chat_request(self, mock_post):
        """Test successful chat request"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'Test response'
                }
            }]
        }
        mock_post.return_value = mock_response

        response = self.client.post('/chat',
                                  data=json.dumps({'message': 'Test message'}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['response'], 'Test response')

    @patch('app.requests.post')
    def test_api_error_handling(self, mock_post):
        """Test API error handling"""
        # Mock API error
        mock_post.side_effect = Exception('API Error')

        response = self.client.post('/chat',
                                  data=json.dumps({'message': 'Test message'}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')

    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        # Temporarily disable testing mode to test rate limiting
        app.config['TESTING'] = False
        try:
            # Test multiple requests
            for _ in range(51):  # Exceed rate limit (50 requests/hour)
                response = self.client.post('/chat',
                                          data=json.dumps({'message': 'Test'}),
                                          content_type='application/json')
            
            # The last request should be rate limited
            self.assertEqual(response.status_code, 429)
            data = json.loads(response.data)
            self.assertIn('Rate limit exceeded', data['error'])
        finally:
            # Restore testing mode
            app.config['TESTING'] = True

if __name__ == '__main__':
    unittest.main()
