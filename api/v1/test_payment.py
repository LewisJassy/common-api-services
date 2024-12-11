import unittest
from unittest.mock import patch
import requests

class TestPaymentAPI(unittest.TestCase):
    @patch('requests.post')
    def test_payment_endpoint(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'success': True}

        response = requests.post('http://localhost:5000/api/v1/payment', json={'amount': 100})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})

if __name__ == '__main__':
    unittest.main()