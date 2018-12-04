from decimal import Decimal

import pytest

from booking.aio.payments import save_transaction
from booking.exceptions import NoExchangeRateError

pytestmark = [pytest.mark.usefixtures("database"), pytest.mark.asyncio]


@pytest.fixture
def setup_rates(mocker):
    def inner(value):
        async def coro():
            if isinstance(value, Exception):
                raise value
            return value

        mocker.patch("booking.aio.exchange.to_eur", return_value=coro())

    return inner


async def test_save_transaction(setup_rates):
    setup_rates(Decimal(100))
    transaction = await save_transaction(1, Decimal(2550), "CZK")
    assert transaction.amount_eur == Decimal(100)


async def test_save_transaction_no_rates(setup_rates):
    setup_rates(NoExchangeRateError("No such rate"))
    with pytest.raises(NoExchangeRateError, message="No such rate"):
        await save_transaction(1, Decimal(10), "NOK")
