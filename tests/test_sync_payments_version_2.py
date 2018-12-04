from decimal import Decimal

import pytest

from booking.exceptions import NoExchangeRateError
from booking.sync.payments import save_transaction

pytestmark = [pytest.mark.usefixtures("database")]


@pytest.fixture
def setup_rates(mocker):
    def inner(**kwargs):
        mocker.patch("booking.sync.exchange.to_eur", **kwargs)

    return inner


def test_save_transaction(setup_rates):
    setup_rates(return_value=Decimal(100))
    transaction = save_transaction(1, Decimal(2550), "CZK")
    assert transaction.amount_eur == 100


def test_save_transaction_no_rates(setup_rates):
    setup_rates(side_effect=NoExchangeRateError("No such rate"))
    with pytest.raises(NoExchangeRateError, message="No such rate"):
        save_transaction(1, Decimal(10), "NOK")
