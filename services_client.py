import requests
import os
from typing import Dict, Any, List


API_URL = os.getenv("INDOSMM_API_URL", "https://indosmm.id/api/v2")
API_KEY = os.getenv("INDOSMM_API_KEY", "")


class IndosmmClient:
def __init__(self, api_key: str = API_KEY, api_url: str = API_URL):
self.api_key = api_key
self.api_url = api_url


def _post(self, payload: Dict[str, Any]):
data = {"key": self.api_key, **payload}
r = requests.post(self.api_url, data=data, timeout=30)
r.raise_for_status()
return r.json()


def balance(self):
return self._post({"action": "balance"})


def services(self) -> List[Dict[str, Any]]:
return self._post({"action": "services"})


def add_order(self, service: int, link: str, quantity: int, runs: int=None, interval: int=None):
payload = {"action": "add", "service": service, "link": link, "quantity": quantity}
if runs: payload["runs"] = runs
if interval: payload["interval"] = interval
return self._post(payload)


def status(self, order_id: str):
return self._post({"action": "status", "order": order_id})


def status_multi(self, order_ids: str):
return self._post({"action": "status", "orders": order_ids})


def refill(self, order_id: str=None, orders_csv: str=None):
if order_id:
return self._post({"action": "refill", "order": order_id})
return self._post({"action": "refill", "orders": orders_csv})


def refill_status(self, refill_id: str=None, refills_csv: str=None):
if refill_id:
return self._post({"action": "refill_status", "refill": refill_id})
return self._post({"action": "refill_status", "refills": refills_csv})


def cancel(self, orders_csv: str):
return self._post({"action": "cancel", "orders": orders_csv})
