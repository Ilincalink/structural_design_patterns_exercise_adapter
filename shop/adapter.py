
"""Implement the Adapter(s) so our app can speak to 3rd-party SDKs.

Goal: Make StripeAPI and PayPalClient usable via the PaymentProcessor interface without
changing the app code in app.checkout.
"""
from .payments import PaymentProcessor
from .third_party_providers import StripeAPI, PayPalClient

class StripeAdapter(PaymentProcessor):
    """Adapt StripeAPI(charge amount_cents) -> dict to PaymentProcessor(pay amount_eur) -> str."""
    def __init__(self, client: StripeAPI):
        self.client = client

    def pay(self, amount: float) -> str:
        # StripeAPI expects amount in cents (int), so convert EUR to cents
        amount_cents = int(round(amount * 100))
        result = self.client.charge(amount_cents)
        if result.get("status") == "success":
            return f"paid {amount:.2f} EUR via Stripe ({self.client.account_email})"
        else:
            raise Exception("Stripe payment failed")

class PayPalAdapter(PaymentProcessor):
    """Adapt PayPalClient(make_payment total: float) -> (bool, total) to PaymentProcessor interface."""
    def __init__(self, client: PayPalClient):
        self.client = client

    def pay(self, amount: float) -> str:
        success, total = self.client.make_payment(amount)
        if success:
            return f"paid {total:.2f} EUR via PayPal ({self.client.merchant_email})"
        else:
            raise Exception("PayPal payment failed")
        # - Validate the success flag
        # - Return: "paid 12.34 EUR via PayPal (merchant@example.com)"
        raise NotImplementedError
