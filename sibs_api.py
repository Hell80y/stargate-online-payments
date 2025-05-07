import os
import requests
from dotenv import load_dotenv

load_dotenv()

SIBS_BEARER_TOKEN = os.getenv("SIBS_BEARER_TOKEN")
SIBS_TERMINAL_ID = os.getenv("SIBS_TERMINAL_ID")
SIBS_MERCHANT_ID = os.getenv("SIBS_MERCHANT_ID")
SIBS_API_URL = os.getenv("SIBS_API_URL", "https://stargate-cer.qly.site1.sibs.pt")

def create_payment_link(amount, order_id, description):
    url = f"{SIBS_API_URL}/api/v1/link-to-pay/create"

    headers = {
        "Authorization": f"Bearer {SIBS_BEARER_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "paymentInfo": {
            "merchantId": SIBS_MERCHANT_ID,
            "acceptorId": "1",
            "terminalId": SIBS_TERMINAL_ID,
            "amount": {
                "value": int(amount * 100),
                "currency": "EUR"
            },
            "validity": "DY90",
            "linkType": "SNGL",
            "paymentMethods": ["CARD"],
            "reference": order_id,
            "description": description
        },
        "dataCollection": {
            "customerInfo": {
                "customerName": True,
                "customerEmail": True
            },
            "billingAddressInfo": {
                "billingAddressCollection": False,
                "billingCityCollection": False,
                "billingPostalCodeCollection": False,
                "billingCountryCollection": False
            },
            "shippingAddressInfo": {
                "shippingAddressCollection": False,
                "shippingCityCollection": False,
                "shippingPostalCodeCollection": False,
                "shippingCountryCollection": False
            },
            "customMerchantInfo": {
                "parameters": {
                    "tag": "t1",
                    "label": "tag",
                    "format": "jpg"
                }
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    try:
        response.raise_for_status()
        data = response.json()
        return data.get("redirectUrl") or data.get("paymentLinkUrl") or data
    except Exception as e:
        print("❌ SIBS API Error:", e)
        print("🔍 Response body:", response.text)
        raise
