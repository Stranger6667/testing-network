from decimal import Decimal

import pytest

from booking.exceptions import NoExchangeRateError
from booking.sync.payments import save_transaction

pytestmark = [pytest.mark.usefixtures("database")]


@pytest.fixture
def setup_rates(pook):
    def inner(**kwargs):
        pook.get("http://127.0.0.1:5000/to_eur", **kwargs)

    yield inner


def test_save_transaction(setup_rates):
    setup_rates(response_json={"result": 100})
    transaction = save_transaction(1, Decimal(2550), "CZK")
    assert transaction.amount_eur == 100


def test_save_transaction_no_rates(setup_rates):
    setup_rates(response_json={"detail": "No such rate"}, response_status=400)
    with pytest.raises(NoExchangeRateError, message="No such rate"):
        save_transaction(1, Decimal(10), "NOK")
