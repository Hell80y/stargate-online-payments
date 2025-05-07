import os
import requests
from dotenv import load_dotenv

load_dotenv()

SIBS_BEARER_TOKEN = os.getenv("SIBS_BEARER_TOKEN")
SIBS_TERMINAL_ID = os.getenv("SIBS_TERMINAL_ID")
SIBS_API_URL = os.getenv("SIBS_API_URL", "https://stargate-cer.qly.site1.sibs.pt")


def create_payment_link(amount, order_id, description):
    url = f"{SIBS_API_URL}/checkout/link"

    headers = {
        "Authorization": f"Bearer {SIBS_BEARER_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "terminalId": SIBS_TERMINAL_ID,
        "transactionType": "payment",
        "amount": int(amount * 100),
        "currency": "EUR",
        "merchantTransactionId": order_id,
        "description": description,
        "callbackUrl": "https://yourdomain.com/payment-callback",
        "successUrl": "https://yourdomain.com/payment-success",
        "failUrl": "https://yourdomain.com/payment-fail"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json().get("redirectUrl")
