from decimal import Decimal

import pytest

from booking.aio.payments import save_transaction
from booking.exceptions import NoExchangeRateError

pytestmark = [pytest.mark.usefixtures("database"), pytest.mark.asyncio]


async def test_save_transaction(mocker):
    async def coro():
        return Decimal(100)

    mocker.patch("booking.aio.exchange.to_eur", return_value=coro())
    transaction = await save_transaction(1, Decimal(2550), "CZK")
    assert transaction.amount_eur == Decimal(100)


async def test_save_transaction_no_rates(mocker):
    async def coro():
        raise NoExchangeRateError("No such rate")

    mocker.patch("booking.aio.exchange.to_eur", return_value=coro())
    with pytest.raises(NoExchangeRateError, message="No such rate"):
        await save_transaction(1, Decimal(10), "NOK")
