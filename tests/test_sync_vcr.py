from decimal import Decimal

import pytest

from booking.exceptions import NoExchangeRateError
from booking.sync.payments import save_transaction

pytestmark = [pytest.mark.usefixtures("database"), pytest.mark.vcr]


def test_save_transaction():
    transaction = save_transaction(1, Decimal(2550), "CZK")
    assert transaction.amount_eur == Decimal(100)


def test_save_transaction_no_rates():
    with pytest.raises(NoExchangeRateError, message="No such rate"):
        save_transaction(1, Decimal(10), "NOK")
