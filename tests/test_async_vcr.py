from decimal import Decimal

import pytest

from booking.aio.payments import save_transaction
from booking.exceptions import NoExchangeRateError

pytestmark = [pytest.mark.usefixtures("database"), pytest.mark.vcr, pytest.mark.asyncio]


async def test_save_transaction_async():
    transaction = await save_transaction(1, Decimal(2550), "CZK")
    assert transaction.amount_eur == Decimal(100)


async def test_save_transaction_no_rates_async():
    with pytest.raises(NoExchangeRateError, message="No such rate"):
        await save_transaction(1, Decimal(10), "NOK")
