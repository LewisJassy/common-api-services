import unittest
from unittest.mock import patch, MagicMock
from payment import PaymentProcessor

class TestPaymentProcessor(unittest.TestCase):

    @patch('stripe.PaymentIntent.create')
    def test_stripe_payment(self, mock_create):
        mock_create.return_value = {'id': 'pi_12345', 'status': 'succeeded'}
        processor = PaymentProcessor()
        response = processor.stripe_payment(1000, 'usd', 'pm_card_visa', 'Test payment')
        self.assertEqual(response['id'], 'pi_12345')
        self.assertEqual(response['status'], 'succeeded')

    @patch('paypalrestsdk.Payment.create')
    def test_paypal_payment(self, mock_create):
        mock_payment = MagicMock()
        mock_payment.create.return_value = True
        # mock_payment.id = 'PAY-12345'
        mock_payment.state = 'approved'
        mock_create.return_value = mock_payment

        processor = PaymentProcessor()
        response = processor.paypal_payment(100, 'USD', 'http://localhost:5000/return', 'http://localhost:5000/cancel')
        # self.assertEqual(response.id, 'PAY-12345')
        self.assertEqual(response.state, 'approved')

    @patch('stripe.Refund.create')
    def test_refund_stripe(self, mock_create):
        mock_create.return_value = {'id': 're_12345', 'status': 'succeeded'}
        processor = PaymentProcessor()
        response = processor.refund_stripe('ch_12345')
        self.assertEqual(response['id'], 're_12345')
        self.assertEqual(response['status'], 'succeeded')

    @patch('paypalrestsdk.Sale.find')
    def test_paypal_refund(self, mock_find):
        mock_refund = MagicMock(id='R-12345', state='completed')
        mock_find.return_value.refund.return_value = mock_refund
        processor = PaymentProcessor()
        response = processor.paypal_refund('SALE-12345', '100.00')
        self.assertEqual(response.id, 'R-12345')
        self.assertEqual(response.state, 'completed')

if __name__ == '__main__':
    unittest.main()