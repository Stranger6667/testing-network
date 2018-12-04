from decimal import Decimal

import pytest
import requests

from booking.exceptions import NoExchangeRateError
from booking.sync.payments import save_transaction

pytestmark = [pytest.mark.usefixtures("database")]


def test_save_transaction(responses):
    responses.add(responses.GET, "http://127.0.0.1:5000/to_eur", body='{"result": "100"}')
    transaction = save_transaction(1, Decimal(2550), "CZK")
    assert transaction.amount_eur == Decimal(100)


def test_save_transaction_no_rates(responses):
    responses.add(responses.GET, "http://127.0.0.1:5000/to_eur", body=NoExchangeRateError("No such rate"))
    with pytest.raises(NoExchangeRateError, message="No such rate"):
        save_transaction(1, Decimal(10), "NOK")


def test_save_transaction_exception(responses):
    responses.add(responses.GET, "http://127.0.0.1:5000/to_eur", body=requests.ConnectionError("Error"))
    with pytest.raises(requests.ConnectionError, message="Error"):
        save_transaction(1, Decimal(10), "NOK")
