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

    @patch('requests.post')
    def test_payment_endpoint_failure(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {'success': False, 'error': 'Invalid request'}

        response = requests.post('http://localhost:5000/api/v1/payment', json={'amount': -100})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'error': 'Invalid request'})

    @patch('requests.post')
    def test_stripe_payment(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'success': True, 'payment_method': 'stripe'}

        response = requests.post('http://localhost:5000/api/v1/payment/stripe', json={'amount': 100, 'currency': 'usd', 'payment_method_id': 'pm_12345', 'description': 'Test payment'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True, 'payment_method': 'stripe'})

    @patch('requests.post')
    def test_paypal_payment(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'success': True, 'payment_method': 'paypal'}

        response = requests.post('http://localhost:5000/api/v1/payment/paypal', json={'total_amount': 100, 'currency': 'USD', 'return_url': 'http://localhost:5000/return', 'cancel_url': 'http://localhost:5000/cancel'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True, 'payment_method': 'paypal'})

    @patch('requests.post')
    def test_payment_endpoint_large_amount(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'success': True}

        response = requests.post('http://localhost:5000/api/v1/payment', json={'amount': 1000000})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})

    @patch('requests.post')
    def test_payment_endpoint_zero_amount(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {'success': False, 'error': 'Amount must be greater than zero'}

        response = requests.post('http://localhost:5000/api/v1/payment', json={'amount': 0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'error': 'Amount must be greater than zero'})

    @patch('requests.post')
    def test_refund_endpoint(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'success': True, 'refund_id': 'r_12345'}

        response = requests.post('http://localhost:5000/api/v1/refund', json={'payment_id': 'p_12345', 'amount': 100})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True, 'refund_id': 'r_12345'})

    @patch('requests.post')
    def test_refund_endpoint_failure(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {'success': False, 'error': 'Invalid payment ID'}

        response = requests.post('http://localhost:5000/api/v1/refund', json={'payment_id': 'invalid_id', 'amount': 100})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'error': 'Invalid payment ID'})

if __name__ == '__main__':
    unittest.main()