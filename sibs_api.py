import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SIBS_BEARER_TOKEN = os.getenv("SIBS_BEARER_TOKEN")
SIBS_TERMINAL_ID = os.getenv("SIBS_TERMINAL_ID")
SIBS_MERCHANT_ID = os.getenv("SIBS_MERCHANT_ID")
SIBS_CLIENT_ID = os.getenv("SIBS_CLIENT_ID")
SIBS_API_URL = os.getenv("SIBS_API_URL", "https://stargate-cer.qly.site1.sibs.pt")

def create_payment_link(amount, order_id, description):
    url = f"{SIBS_API_URL}/api/v1/link-to-pay/create"

    headers = {
        "Authorization": f"Bearer {SIBS_BEARER_TOKEN}",
        "Content-Type": "application/json",
        "X-IBM-Client-Id": SIBS_CLIENT_ID
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

def create_payment_form_transaction(amount, order_id, description, customer_name, customer_email):
    url = f"{SIBS_API_URL}/api/v1/payments"

    headers = {
        "Authorization": f"Bearer {SIBS_BEARER_TOKEN}",
        "Content-Type": "application/json",
        "X-IBM-Client-Id": SIBS_CLIENT_ID
    }

    payload = {
        "merchant": {
            "terminalId": SIBS_TERMINAL_ID,
            "channel": "web",
            "merchantTransactionId": order_id,
            "transactionDescription": description,
            "shopURL": "https://yourshop.com"
        },
        "transaction": {
            "transactionTimestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "description": description,
            "moto": False,
            "paymentType": "PURS",
            "amount": {
                "value": round(amount, 2),
                "currency": "EUR"
            },
            "paymentMethod": ["CARD"]
        },
        "customer": {
            "customerInfo": {
                "customerName": customer_name,
                "customerEmail": customer_email
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    try:
        response.raise_for_status()
        data = response.json()
        return {
            "transaction_id": data["transactionID"],
            "form_context": data["formContext"],
            "amount": round(amount, 2)
        }
    except Exception as e:
        print("❌ Payment Form API Error:", e)
        print("🔍 Response body:", response.text)
        raise