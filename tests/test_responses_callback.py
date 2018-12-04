from decimal import Decimal
import json
from urllib.parse import parse_qsl, urlparse

import pytest

from booking.exceptions import NoExchangeRateError
from booking.sync.payments import save_transaction

pytestmark = [pytest.mark.usefixtures("database")]


@pytest.fixture
def setup_rates(responses):
    def request_callback(request):
        parsed = urlparse(request.url)
        query_string = dict(parse_qsl(parsed.query))
        amount = Decimal(query_string["amount"])
        currency = query_string["currency"]
        rates = {"CZK": Decimal("25.5")}
        try:
            rate = rates[currency]
            result = {"result": str(amount / rate)}
            status = 200
        except KeyError:
            result = {"detail": "No such rate"}
            status = 400
        return status, {}, json.dumps(result)

    responses.add_callback(responses.GET, "http://127.0.0.1:5000/to_eur", callback=request_callback)


@pytest.mark.usefixtures("setup_rates")
def test_save_transaction():
    transaction = save_transaction(1, Decimal(2550), "CZK")
    assert transaction.amount_eur == Decimal(100)


@pytest.mark.usefixtures("setup_rates")
def test_save_transaction_no_rates():
    with pytest.raises(NoExchangeRateError, message="No such rate"):
        save_transaction(1, Decimal(10), "NOK")
