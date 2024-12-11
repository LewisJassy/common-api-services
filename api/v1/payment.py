import stripe
import paypalrestsdk
import os

STRIPEAPI = os.getenv('STRIPE_SECRET_KEY')
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')

class PaymentProcessor:
    def __init__(self):
        stripe.api_key = STRIPEAPI

        paypalrestsdk.configure({
            "mode": "sandbox",
            "client_id": PAYPAL_CLIENT_ID,
            "client_secret": PAYPAL_CLIENT_SECRET
        })

    def stripe_payment(self, amount, currency, payment_method_id, description):
        """Handle Stripe Payment"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
                description=description
            )
            return intent

        except stripe.error.CardError as e:
            return str(e)
        
    def paypal_payment(self, total_amount, currency, return_url, cancel_url):
        """Handle PayPal Payment"""
        try:
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": return_url,
                    "cancel_url": cancel_url
                },
                "transactions": [{
                    "amount": {
                        "total": total_amount,
                        "currency": currency
                    },
                    "description": "Payment for the order."
                }]
            })

            if payment.create():
                return payment
            else:
                return payment.error
                
        except Exception as e:
            return str(e)
        
    def refund_stripe(self, charge_id):
        """Refund a Stripe Payment"""
        try:
            refund = stripe.Refund.create(
                charge=charge_id
            )
            return refund

        except stripe.error.InvalidRequestError as e:
            return str(e)
    
    def paypal_refund(self, sale_id, amount):
        """Refund a PayPal Payment"""
        try:
            refund = paypalrestsdk.Sale.find(sale_id).refund({
                "amount": {
                    "total": amount,
                    "currency": "USD"
                }
            })
            return refund

        except Exception as e:
            return str(e)
        
if __name__ == '__main__':
    processor = PaymentProcessor()

    # Example usage
    # Create a new Stripe payment
    payment = processor.stripe_payment(1000, "usd", "pm_card_visa", "Test payment")
    print("Stripe Payment ID:", payment.id if hasattr(payment, 'id') else payment)

    # Create a new PayPal payment
    payment = processor.paypal_payment(100, "USD", "http://localhost:5000/return", "http://localhost:5000/cancel")
    print("PayPal Payment ID:", payment.id if hasattr(payment, 'id') else payment)