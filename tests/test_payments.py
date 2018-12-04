from decimal import Decimal

import pytest

from booking.default.payments import save_transaction
from booking.exceptions import NoExchangeRateError

pytestmark = [pytest.mark.usefixtures("database")]


def test_save_transaction(exchange_rate_factory):
    exchange_rate_factory(currency="CZK", ratio="25.5")
    transaction = save_transaction(1, Decimal(2550), "CZK")
    assert transaction.amount_eur == Decimal(100)


def test_save_transaction_no_rates():
    with pytest.raises(NoExchangeRateError, message="No such rate"):
        save_transaction(1, Decimal(10), "NOK")
