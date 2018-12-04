from decimal import Decimal

import pytest

from booking.aio.payments import save_transaction
from booking.exceptions import NoExchangeRateError

pytestmark = [pytest.mark.usefixtures("database"), pytest.mark.asyncio]


async def test_save_transaction(pook):
    pook.get("http://127.0.0.1:5000/to_eur", response_json={"result": 100})
    transaction = await save_transaction(1, Decimal(2550), "CZK")
    assert transaction.amount_eur == 100


async def test_save_transaction_no_rates(pook):
    pook.get("http://127.0.0.1:5000/to_eur", response_json={"detail": "No such rate"}, response_status=400)
    with pytest.raises(NoExchangeRateError, message="No such rate"):
        await save_transaction(1, Decimal(10), "NOK")
