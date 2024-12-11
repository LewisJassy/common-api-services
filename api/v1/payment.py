import stripe
import paypalrestsdk
import os


class PaymentProcessor:
    def __init_(self):
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

        paypalrestsdk.configure({
            "mode": "sandbox",
            "client_id": os.getenv('PAYPAL_CLIENT_ID'),
            "client_secret": os.getenv('PAYPAL_CLIENT_SECRET')
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
        
    