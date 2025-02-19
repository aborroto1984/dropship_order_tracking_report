from config import auth_shipstation
from datetime import datetime
import requests

BASE_URL = "https://ssapi.shipstation.com"


def mark_shipped(order_id, tracking_number, carrier_code="fedex"):
    url = f"{BASE_URL}/orders/markasshipped"
    data = {
        "orderId": order_id,
        "carrierCode": carrier_code,
        "shipDate": datetime.today().strftime("%Y-%m-%d"),
        "trackingNumber": tracking_number,
        "notifyCustomer": True,
        "notifySalesChannel": True,
    }
    r = requests.post(url, auth=auth_shipstation, json=data)
    if r.status_code != 200:
        raise ValueError(f"Failed to mark order as shipped: {r.text}")
    return r.text
