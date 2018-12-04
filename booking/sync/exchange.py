from decimal import Decimal

import requests

from ..exceptions import NoExchangeRateError


def to_eur(amount: Decimal, currency: str):
    response = requests.get("http://127.0.0.1:5000/to_eur", params={"amount": amount, "currency": currency})
    data = response.json()
    try:
        response.raise_for_status()
    except requests.HTTPError:
        if data["detail"] == "No such rate":
            raise NoExchangeRateError
        raise
    return Decimal(data["result"])
